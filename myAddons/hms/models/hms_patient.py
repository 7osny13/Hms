from odoo import  models, fields ,api
import re
from odoo.odoo.exceptions import ValidationError,UserError
from datetime import date

class HmsPatient(models.Model) :
    _name = 'hms.patient'
    _oder = "first_name"

    first_name = fields.Char()
    last_name = fields.Char()
    birthdate = fields.Date()
    history = fields.Html()
    ratio = fields.Integer()
    Blood_type = fields.Selection([('A+' , 'A+'), ('A-' , 'A-'), ('AB' , 'AB'), ('B-' , 'B-')] ,default = 'A+')
    age = fields.Integer(compute='calc_age')
    address = fields.Text()
    image = fields.Image()
    pcr = fields.Boolean()
    status=fields.Selection([('Undtermine' , 'Undtermine'), ('Good' , 'Good'), ('Fair' , 'Fair'), ('Serious' , 'Serious')] )
    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related="department_id.capacity")
    email = fields.Char()
    log_ids=fields.One2many('hms.patientlog','patient_id')


    _sql_constraints=[

        ('emial_unique' , 'UNIQUE(email)' , 'email must be unique')
    ]

    def go_to_undetermined(self):
        self.state = "Undtermine"

        self.env['hms.log'].create({'description': "history of patient is undtermined", 'patient_id': self.id})

    def go_to_good(self):
        self.state = "Good"
        self.env['hms.log'].create({'description': "history of patient is good", 'patient_id': self.id})

    def go_to_fair(self):
        self.state = "Fair"
        self.env['hms.log'].create({'description': "history of patient is fair", 'patient_id': self.id})

    def go_to_serious(self):
        self.state = "Serious"
        self.env['hms.log'].create({'description': "history of patient is serious", 'patient_id': self.id})

    @api.depends('birthdate')
    def calc_age(self):
        for rec in self:
            if rec.birthdate:
                rec.age=date.today().year - rec.birthdate.year
            else:
                rec.age=0

    @api.onchange('email')
    def validate_email(self):
        match={}
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$' , self.email)
        if match==None:
           raise ValidationError("email not valid")


    @api.constrains('birthdate')
    def check_birthday(self):
        if self.birthdate > date.today():
            raise ValidationError("birthday cannot be greater than today")


    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30 :
            self.pcr = True
            return{
                'warning':{
                'title':"age warning",
                'message':"age lower than 30"
                }
            }
        else:
            self.pcr = False






