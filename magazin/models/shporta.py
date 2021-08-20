from odoo import fields, models, api
from odoo.exceptions import UserError


class Shporta(models.Model):
    _inherit = 'shporta'

    magazina_id = fields.Many2one(comodel_name='magazin.magazina', string='Magazina_id', required=True)
    sasia_id = fields.Many2one('magazin.sasia', compute='gjej_sasia_id', store=True)

    @api.multi
    @api.depends('magazina_id', 'produkti')
    def gjej_sasia_id(self):
        for shporta in self:
            sasia_id = self.env['magazin.sasia'].search([('produkt_id', '=', res.produkti.id), ('magazina_id', '=', shporta.magazina_id.id)]).mapped('name') if shporta.magazina_id else None

    @api.model
    def create(self, values):
        res = super(Shporta, self.with_context(**{'inherited_mag': True})).create(values)
        if values.get('sasia') > res.sasia_id.sasia or values.get('sasia') <= 0:
            search = self.env['magazin.sasia'].search([('produkt_id', '=', res.produkti.id), ('sasia', '>=', res.sasia)]).mapped('name')
            if search:
                magazinat_lira = ', '.join(search)
                raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Magazinat qe suportojn sasine e caktuar: '.format(res.produkti.name, res.magazina_id.name, magazinat_lira))
            else:
                raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Asnje magazine nuk e suporton dot sasine e kerkuar.'.format(res.produkti.name, res.magazina_id.name))
        else:
            res.sasia_id.sasia = res.sasia_id.sasia - values.get('sasia')
        return res

    @api.multi
    def write(self, vals):
        for shporte in self:
            sasia = vals.get('sasia', 0) - shporte.sasia
            if sasia > 0:
                search = self.env['magazin.sasia'].search([('produkt_id', '=', shporte.produkti.id), ('sasia', '>=', sasia)]).mapped('name')
                if search and vals.get('sasia') > shporte.sasia_id.sasia:
                    magazinat_lira = ', '.join(search)
                    raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Magazinat qe suportojn sasine e caktuar: '.format(shporte.produkti.name, shporte.magazina_id.name, magazinat_lira))
                else:
                    raise UserError('Sasia qe kerkohet te blihet per produktin {} nuk ka ne magazinen {}. Asnje magazine nuk e suporton dot sasine e kerkuar.'.format(shporte.produkti.name, shporte.magazina_id.name))
            else:
                shporte.sasia_id.sasia = shporte.sasia_id.sasia - sasia
            return super(Shporta, shporte.with_context(**{'inherited_mag':True})).write(vals)

    @api.multi
    def unlink(self):
        for shporte in self:
            shporte.produkti.magazinat_ids.sasia += shporte.sasia
            return super(Shporta, shporte.with_context(**{'inherited_mag':True})).unlink()
