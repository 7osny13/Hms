from odoo import models , fields



class PatientLog(models.Model):

    _name = 'hms.patientlog'

    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')