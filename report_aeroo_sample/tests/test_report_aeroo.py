# -*- coding: utf-8 -*-
# © 2016 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo.tests import common


class TestAerooReport(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAerooReport, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'My Partner',
            'lang': 'en_US',
        })
        cls.report = cls.env.ref('report_aeroo_sample.aeroo_sample_report_id')

    def test_01_sample_report_doc(self):
        self.report.out_format = self.env.ref(
            'report_aeroo.report_mimetypes_doc_odt')
        self.partner.print_report('sample_report', {})

    def test_02_sample_report_pdf(self):
        self.report.out_format = self.env.ref(
            'report_aeroo.report_mimetypes_pdf_odt')
        self.partner.print_report('sample_report', {})

    def test_03_sample_report_pdf_by_lang(self):
        self.report.write({
            'tml_source': 'lang',
            'lang_eval': 'o.lang',
        })
        self.report.report_line_ids = [(0, 0, {
            'lang_id': self.env.ref('base.lang_en').id,
            'template_source': 'file',
            'template_location': 'report_aeroo_sample/report/template.odt',
        })]
        self.report.out_format = self.env.ref(
            'report_aeroo.report_mimetypes_pdf_odt')
        self.partner.print_report('sample_report', {})