from odoo import api,models, fields,_ # type: ignore
from odoo.exceptions import UserError,ValidationError # type: ignore
import base64

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']  
    _description = 'Patient Records'
    _rec_name = 'patient_name'

    patient_name = fields.Char(string="Name", required=True, track_visibility='onchange',tracking=True)
    date_of_birth = fields.Date(string='DOB',tracking=True)
    patient_age = fields.Integer(string="Age", track_visibility='onchange')
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Image")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    logo_image = fields.Binary(string="Add Image")

    tag_ids = fields.Many2many('patient.tag','patient_tag_rel','patient_id','tag_id',string="Tags")
    
    is_miner = fields.Boolean(string='Miner')
    guardian = fields.Char(string='Guardian')
    weight = fields.Float(string="Weight")

    def test_name(self):
    
        return True
    
    def create_appointment(self):
    
        return True
    
    def action_print_patient_report(self):
    
        return self.env.ref('hospital.action_report_patient').report_action(self)
     
    @api.ondelete(at_uninstall=False)
    def _check_patient_appointments(self):
        for rec in self:
            domain =[('patient_id','=','rec.id')]
            appointments=self.env['hospital.appointment'].search(domain)
            if appointments:
                raise ValidationError(_('You can not delete.Appointment exist'))
            
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hospital.patient'].browse(docids)
        for doc in docs:
            if doc.image:
                doc.image = base64.b64encode(doc.image).decode('utf-8')
            if doc.logo_image:  # Convert binary logo to base64 string
                doc.logo_image = base64.b64encode(doc.logo_image).decode('utf-8')

        return {
            'doc_ids': docids,
            'doc_model': 'hospital.patient',
            'docs': docs,
        }
            
    # @api.model
    # def unlink(self):
    #     for patient in self:
    #         # Find and unlink appointments first
    #         appointments = self.env['hospital.appointment'].search([('patient_id', '=', patient.id)])
    #         if appointments:
    #             appointments.unlink()  # Remove the appointments
    #         # Proceed to delete the patient record
    #     return super(HospitalPatient, self).unlink(self)

