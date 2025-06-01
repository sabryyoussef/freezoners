from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


from odoo import models, fields

class DocumentsShareWizard(models.Model):
    _name = 'documents.share.wizard'
    _description = 'Documents Share Wizard'

    task_ids = fields.Many2many('project.task', string='Tasks')


    document_share_id = fields.Many2one('documents.share', string='Documents Share')
    summary = fields.Char(string='Summary', required=True)
    date_from = fields.Datetime(string='Start Date', required=True)
    date_to = fields.Datetime(string='End Date', required=True)
    assigned_to_id = fields.Many2one('res.users', string='Assigned To', required=True)
    activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type', required=True)

    @api.model
    def default_get(self, fields):
        res = super(DocumentsShareWizard, self).default_get(fields)
        res['document_share_id'] = self.env.context.get('active_id')
        return res

    def create_activity(self):
        partners = [self.document_share_id.document_ids[0].partner_id.id, self.create_uid.partner_id.id]
        partner_commands = [(6, 0, partners)]
        alarm_commands = [(6, 0, [1, 2])]
        calendar_event = self.env['calendar.event'].create({
            'name': self.summary,
            'start': self.date_from,
            'stop': self.date_to,
            'user_id': self.assigned_to_id.id,
            'show_as': 'free',
            'partner_ids': partner_commands,
            'alarm_ids': alarm_commands,
            'document_share_id': self.document_share_id.id,
        })
        self.env['mail.activity'].create({
            'activity_type_id': self.activity_type_id.id,
            'summary': self.summary,
            'date_deadline': self.date_to,
            'user_id': self.assigned_to_id.id,
            'calendar_event_id': calendar_event.id,
            'res_id': self.document_share_id.id,
            'res_model_id': self.env['ir.model']._get('documents.share').id,
        })
        return calendar_event