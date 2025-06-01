from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class DocumentsShare(models.Model):
    _name = 'documents.share'
    _description = 'Document Share'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    number = fields.Char(
        string='Number', required=True, copy=False, readonly=True,
        index=True, default=lambda self: _('New'))
    full_url = fields.Char(string='Full URL', compute='_compute_full_url', store=True)
    access_token = fields.Char(string='Access Token', required=True, copy=False, default=lambda self: self._generate_access_token())
    can_upload = fields.Boolean(string='Can Upload', default=False, tracking=True,
        help="Allow users to upload documents through the share link")
    partner_id = fields.Many2one('res.partner', string='Partner', tracking=True)
    owner_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, tracking=True)
    folder_id = fields.Many2one('documents.folder', string='Folder', tracking=True)
    document_ids = fields.Many2many('documents.document', string='Documents', tracking=True)
    type = fields.Selection([
        ('ids', 'Selected Documents'),
        ('domain', 'Workspace')
    ], string='Share Type', required=True, default='ids', tracking=True)
    action = fields.Selection([
        ('download', 'Download'),
        ('upload', 'Upload')
    ], string='Action', required=True, default='download', tracking=True)
    date_deadline = fields.Date(string='Expiration Date', tracking=True)
    email_drop = fields.Boolean(string='Email Drop', default=False)
    alias_id = fields.Many2one('mail.alias', string='Email Alias')
    alias_name = fields.Char(string='Alias Name')
    alias_domain = fields.Char(string='Alias Domain', related='alias_id.alias_domain')
    include_sub_folders = fields.Boolean(string='Include Sub-folders', default=False)
    tag_ids = fields.Many2many('documents.tag', string='Tags')
    activity_option = fields.Boolean(string='Schedule Activity', default=False)
    activity_summary = fields.Char(string='Summary')
    activity_date_deadline_range = fields.Integer(string='Due Date In')
    activity_date_deadline_range_type = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')
    ], string='Due type', default='days')
    activity_user_id = fields.Many2one('res.users', string='Assigned to')
    activity_note = fields.Html(string='Note')
    lead_id = fields.Many2one('crm.lead')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'number' not in vals:
                vals['number'] = self.env['ir.sequence'].next_by_code('documents.share') or _('New')
        return super(DocumentsShare, self).create(vals_list)

    def write(self, values):
        res = super(DocumentsShare, self).write(values)
        if not self.env.user.has_group('documents.group_documents_manager'):
            raise ValidationError(_('You do not have access to edit'))
        return res

    @api.onchange('partner_id')
    def _onchange_related_partner_documents(self):
        for rec in self:
            if rec.partner_id:
                # Fetch documents linked to the new partner
                new_documents = self.env['documents.document'].sudo().search(
                    [('partner_id', '=', rec.partner_id.id)]
                )
                # Update only if documents are different from current
                if rec.document_ids != new_documents:
                    rec.document_ids = new_documents

    def open_create_activity_popup(self):
        return {
            'res_model': 'files.activity.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            # 'context': {'default_sub_folder_file_id': self.id},
            'view_id': self.env.ref("cabinet_directory.cabinet_meeting_form_view").id,
            'target': 'new'
        }

    def send_email_activity(self):
        self.ensure_one()  # Ensure it's called on a single record
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': self._name,  # The model of the current record
                'default_res_id': self.id,  # The ID of the current record
                'default_subject': self.name,  # Pass subject from the current record
                'default_partner_ids': [self.partner_id.id],  # Pass subject from the current record
                'default_composition_mode': 'comment',
            }
        }

    def action_schedule_meeting(self, smart_calendar=True):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")
        partner_ids = self.env.user.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        current_opportunity_id = self.lead_id.id or False

        # Add the domain to filter events by the document_share_id
        action['domain'] = [('document_share_id', '=', self.id)]

        action['context'] = {
            'search_default_opportunity_id': current_opportunity_id,
            'default_opportunity_id': current_opportunity_id,
            'default_partner_id': self.partner_id.id,
            'default_partner_ids': partner_ids,
            'default_name': self.name,
            'default_document_share_id': self.id,  # Pass the document_share_id to the new event
        }
        # 'Smart' calendar view: get the most relevant time period to display to the user.
        # if current_opportunity_id and smart_calendar:
        #     mode, initial_date = self._get_opportunity_meeting_view_parameters()
        #     action['context'].update({'default_mode': mode, 'initial_date': initial_date})
        return action

    @api.model
    def open_share_popup(self, vals):
        new_context = dict(self.env.context)
        new_context.update({
            'default_owner_id': self.env.uid,
            'default_folder_id': vals.get('folder_id'),
            'default_tag_ids': vals.get('tag_ids'),
            'default_type': vals.get('type', 'domain'),
            'default_domain': vals.get('domain') if vals.get('type', 'domain') == 'domain' else False,
            'default_document_ids': vals.get('document_ids', False),
        })
        # Use the FULL form view (not popup)
        view_id = self.env.ref('freezoner_custom.share_view_form_new_popup').id  # Changed from 'share_view_form_popup'
        return {
            'type': 'ir.actions.act_window',
            'name': _('Share selected files') if vals.get('type') == 'ids' else _('Share selected workspace'),
            'res_model': 'documents.share',
            'res_id': self.id if self else False,
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'target': 'current',  # Changed from 'new'
            'context': new_context,
        }

    @api.depends('access_token')
    def _compute_full_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for share in self:
            share.full_url = f"{base_url}/document/share/{share.access_token}"

    def _generate_access_token(self):
        return self.env['ir.sequence'].next_by_code('documents.share.token') or self.env['ir.sequence'].sudo().create({
            'name': 'Document Share Token',
            'code': 'documents.share.token',
            'prefix': '',
            'padding': 32,
            'number_increment': 1,
            'company_id': False,
        }).next_by_code('documents.share.token')


class Documents(models.Model):
    _inherit = 'documents.document'

    project_id = fields.Many2one('project.project')
    required_project_id = fields.Many2one('project.project')
    deliverable_project_id = fields.Many2one('project.project')
    issue_date = fields.Date(required=True, tracking=True)
    type_id = fields.Many2one(comodel_name='res.partner.document.type', tracking=True)
    expiration_date = fields.Date(tracking=True)
    partner_ids = fields.Many2many("res.partner", relation="project_partner_id1",
                                   column1="project_partner_id2", column2="project_partner_id3",
                                   string="Partners",
                                   compute='get_project_partners' )
    partner_id = fields.Many2one('res.partner')
    task_ids = fields.Many2one(
        'project.task',
        string='Task',
        ondelete='cascade',
        index=True,
        help='Related task'
    )

    @api.depends('project_id', 'required_project_id', 'deliverable_project_id')
    def get_project_partners(self):
        for rec in self:
            project = rec.project_id or rec.required_project_id or rec.deliverable_project_id
            if project:
                # partners = project.compliance_shareholder_ids.mapped('contact_id.id')
                project_partner_id = project.partner_id.id if project.partner_id else False
                # hand_partner_id = project.hand_partner_id.id if project.hand_partner_id else False
                # partner_list = [pid for pid in [project_partner_id, hand_partner_id] if pid] + partners
                # rec.partner_ids = [(6, 0, partner_list)]
            else:
                rec.partner_ids = [(6, 0, self.env['res.partner'].search([]).ids)]

