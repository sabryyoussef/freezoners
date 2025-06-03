from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class CrmLead(models.Model):
    _inherit = "crm.lead"

    AVAILABLE_PRIORITIES = [
        ("0", "Low"),
        ("1", "Medium"),
        ("2", "High"),
        ("3", "Very High"),
    ]

    SERVICE_SELECTION = [
        ("free", "Free Consultation"),
        ("business_setup", "Business Setup"),
        ("freelance", "Freelance Permit Setup"),
        ("bank", "Bank Account Setup"),
        ("accounting", "Accounting Services"),
        ("marketing", "Marketing Services"),
        ("golden", "Golden Visa"),
        ("pro", "PRO Services"),
        ("service_interested", "Service Interested"),
        ("ksa_business", "KSA Business Setup"),
    ]

    referred_id = fields.Many2one("res.partner", string="Referred By")
    # is_hide_quotation_button = fields.Boolean(
    #     related="stage_id.is_hide_quotation_button", store=True
    # )
    is_hide_quotation_button = fields.Boolean(store=True)
    is_required_referred = fields.Boolean(
        related="source_id.is_required_referred", store=True
    )
    mail_sent = fields.Boolean()
    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string="Heat", index=True, default="0"
    )
    service = fields.Selection(
        SERVICE_SELECTION, string="Service Interested In", index=True, default="free"
    )
    nationality_id = fields.Many2one("res.country")
    # stage_name = fields.Char(related="stage_id.name", store=True)
    stage_name = fields.Char(
        string="Stage Name",
        store=True,
        readonly=False,
    )
    customer_status = fields.Selection(
        [
            ("approved", "Customer Approved"),
            ("approved_reservations", "Customer Approved with Reservations"),
            ("deferred", "Customer Deferred"),
            ("non_responsive", "Customer Non-Responsive"),
        ],
        default="",
        string="Customer Status",
    )
    salesperson_notes = fields.Text("Salesperson Notes")
    lead_ref = fields.Char(
        string="Number",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
        tracking=True,
    )
    employee_id = fields.Many2one("hr.employee")
    business_proposal = fields.Many2one(
        "documents.document", string="Business Proposal", tracking=True
    )
    # is_quotation_expired = fields.Boolean(
    #     compute="_compute_is_quotation_expired", store=True
    # )
    is_hide_quotation_button = fields.Boolean(
        string='Hide “New Quotation” Button'
    )

    def action_view_document(self):
        recs = self.business_proposal
        if not recs:
            return {"type": "ir.actions.act_window_close"}
        action = self.env.ref("documents.document_action").read()[0]
        action["views"] = [
            (self.env.ref("documents.document_view_kanban").id, "kanban"),
            (self.env.ref("documents.documents_view_list").id, "tree"),
            (self.env.ref("documents.document_view_form").id, "form"),
        ]
        action["view_mode"] = "kanban,tree,form"
        action["domain"] = [("id", "in", recs.ids)]
        return action

    @api.depends("date_closed")
    def _compute_is_quotation_expired(self):
        today = fields.Date.today()
        for lead in self:
            lead.is_quotation_expired = bool(
                lead.date_closed and lead.date_closed <= today - relativedelta(months=6)
            )

    @api.model
    def create(self, vals):
        if not vals.get("source_id"):
            raise ValidationError(_("Please add source"))
        vals["lead_ref"] = self.env["ir.sequence"].next_by_code("crm.lead") or _("New")
        return super().create(vals)

    def action_convert_opportunity(self):
        for lead in self:
            if not lead.email_from and not lead.phone:
                raise ValidationError(
                    _("Please make sure to add a phone number or/and an Email")
                )
            return {
                "res_model": "crm.lead2opportunity.partner",
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "view_id": self.env.ref("crm.view_crm_lead2opportunity_partner").id,
                "target": "new",
            }

    def _get_country_codes(self):
        countries = self.env["res.country"].search([])
        return [
            (country.code, f"{country.name} ({country.code})") for country in countries
        ]

    @api.depends("country_code")
    def _compute_mobile_country_code(self):
        for record in self:
            if record.country_code:
                selected_country = self.env["res.country"].search(
                    [("code", "=", record.country_code)], limit=1
                )
                record.mobile_country_code = (
                    "+" + str(selected_country.phone_code)
                    if selected_country
                    else False
                )
            else:
                record.mobile_country_code = False

    @api.depends("country_code")
    def _compute_code(self):
        for lead in self:
            lead.code = lead.country_code or ""

    country_code = fields.Selection(
        selection="_get_country_codes", string="Country Code"
    )
    code = fields.Char(compute="_compute_code", string="Code")
    mobile_country_code = fields.Char(
        string="Mobile Country Code", compute="_compute_mobile_country_code"
    )
    custom_phone = fields.Char(string="Enter Phone")
    phone = fields.Char(string="Phone", compute="_compute_custom_phone", store=True)

    @api.depends("custom_phone", "mobile_country_code")
    def _compute_custom_phone(self):
        for rec in self:
            rec.phone = (
                f"{rec.mobile_country_code}{rec.custom_phone}"
                if rec.mobile_country_code and rec.custom_phone
                else ""
            )

    @api.constrains("custom_phone", "code")
    def _phone_number_constraints(self):
        length_constraints = {
            "EG": 10,
            "LB": 10,
            "AE": 9,
            "SA": 9,
            "US": 12,
            "DE": 12,
            "GB": 11,
        }
        for rec in self:
            if rec.custom_phone:
                required_length = length_constraints.get(rec.code)
                if required_length and len(rec.custom_phone) != required_length:
                    raise ValidationError(
                        _("Please make sure to enter %d digits") % required_length
                    )

            if not rec.email_from and not rec.custom_phone:
                raise ValidationError(
                    _("Please make sure to add a phone number or/and an Email")
                )

            attachments = self.env["documents.document"].search(
                [
                    ("res_model", "=", "crm.lead"),
                    ("res_id", "=", rec.id),
                ]
            )
            if not attachments:
                raise ValidationError(_("Please attach at least one Proposal"))

    def action_check_attachments(self):
        for lead in self:
            attachments = self.env["documents.document"].search(
                [
                    ("res_model", "=", "crm.lead"),
                    ("res_id", "=", lead.id),
                ]
            )
            if not attachments:
                raise ValidationError(_("Please attach at least one Proposal"))

    def action_stage(self):
        for rec in self:
            call = (
                self.env["mail.message"]
                .sudo()
                .search(
                    [
                        ("model", "=", "crm.lead"),
                        ("res_id", "=", rec.id),
                        ("body", "ilike", "Call"),
                    ]
                )
            )
            mails = (
                self.env["mail.mail"]
                .sudo()
                .search(
                    [
                        ("model", "=", "crm.lead"),
                        ("res_id", "=", rec.id),
                    ]
                )
            )
            attachments = (
                self.env["ir.attachment"]
                .sudo()
                .search(
                    [
                        ("res_model", "=", "crm.lead"),
                        ("res_id", "=", rec.id),
                    ]
                )
            )

            if rec.stage_id.name == "New":
                if not rec.email_from and not rec.custom_phone:
                    raise ValidationError(
                        _("Please make sure to add a phone number or/and an Email")
                    )
            elif rec.stage_id.name == "In Contact":
                if not mails and not call:
                    raise ValidationError(
                        _("Please make sure to log a Call or send an Email")
                    )
            elif rec.stage_id.name == "Negotiation":
                if not attachments:
                    raise ValidationError(_("Please attach at least one Proposal"))

            return {
                "res_model": "crm.wizard",
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "context": {"default_crm_id": rec.id},
                "view_id": self.env.ref("crm_log.crm_wizard_form_view").id,
                "target": "new",
            }
