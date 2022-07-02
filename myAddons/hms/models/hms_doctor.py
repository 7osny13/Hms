from odoo import models , fields


class HmsDoctor(models.Model):
    _name= "hms.doctor"

    firstName = fields.Char()
    lastName = fields.Char()
    image = fields.Image()
