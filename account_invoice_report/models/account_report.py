from odoo import models, _
from odoo.tools import format_date, get_lang
from collections import defaultdict


class JournalReportCustomHandler(models.AbstractModel):
    _inherit = "account.journal.report.handler"

    def _get_tax_grids_summary(self, options, data):
        """
        Returns tax grid summaries grouped by country, showing signed balances
        and the net impact per tag.
        """
        report = self.env.ref("account_reports.journal_report")

        tax_report_options = self._get_generic_tax_report_options(options, data)
        tables, where_clause, where_params = report._query_get(
            tax_report_options, "strict_range"
        )

        lang = self.env.user.lang or get_lang(self.env).code

        tag_name_expr = (
            f"COALESCE(tag.name->>'{lang}', tag.name->>'en_US')"
            if hasattr(
                self.env["account.account.tag"].fields_get()["name"], "translate"
            )
            else "tag.name"
        )
        country_name_expr = f"COALESCE(country.name->>'{lang}', country.name->>'en_US')"

        query = f"""
            WITH tag_info (country_name, tag_id, tag_name, tag_sign, balance) AS (
                SELECT
                    {country_name_expr} AS country_name,
                    tag.id,
                    {tag_name_expr} AS tag_name,
                    CASE WHEN tag.tax_negate THEN '-' ELSE '+' END AS tag_sign,
                    SUM(COALESCE(aml.balance, 0) * CASE WHEN aml.tax_tag_invert THEN -1 ELSE 1 END) AS balance
                FROM account_account_tag tag
                JOIN account_account_tag_account_move_line_rel rel ON tag.id = rel.account_account_tag_id
                JOIN res_country country ON country.id = tag.country_id,
                     {tables}
                WHERE {where_clause}
                  AND tag.applicability = 'taxes'
                  AND aml.id = rel.account_move_line_id
                GROUP BY country_name, tag.id
            )
            SELECT
                country_name,
                tag_id,
                REGEXP_REPLACE(tag_name, '^[+-]', '') AS tag_label,
                balance,
                tag_sign
            FROM tag_info
            ORDER BY country_name, tag_label
        """

        self._cr.execute(query, where_params)
        rows = self._cr.fetchall()

        res = defaultdict(lambda: defaultdict(dict))
        sign_opposite = {"+": "-", "-": "+"}

        for country_name, tag_id, tag_label, balance, sign in rows:
            tag_info = res[country_name][tag_label]
            tag_info["tag_id"] = tag_id
            tag_info[sign] = report.format_value(
                balance, blank_if_zero=False, figure_type="monetary"
            )

            if sign_opposite[sign] not in tag_info:
                tag_info[sign_opposite[sign]] = report.format_value(
                    0, blank_if_zero=False, figure_type="monetary"
                )

            tag_info[sign + "_no_format"] = balance
            tag_info["impact"] = report.format_value(
                tag_info.get("+_no_format", 0) - tag_info.get("-_no_format", 0),
                blank_if_zero=False,
                figure_type="monetary",
            )

        return res
