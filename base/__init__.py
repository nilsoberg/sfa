"""An amazing sample package!"""
import logging
import os

from jinja2 import DictLoader, Environment, select_autoescape

__version__ = '0.1'

class Clients:
    def __init__(self, callback_url, clients):
        for client_name, Client in clients.items():
            self.__setattr__(client_name, Client(callback_url))


class Core:
    def __init__(self, ctx, config, clients_class=None):
        ClientsClass = Clients
        if clients_class:
            ClientsClass = clients_class

        self.ctx = ctx
        self.callback_url = config.get("callback_url")
        self.clients = ClientsClass(self.callback_url, config["clients"])
        self.shared_folder = config.get("shared_folder")

    def create_report_from_template(self, template_path, config):
        logging.info("Creating report...")
        # Create report from template
        with open(template_path) as tpf:
            template_source = tpf.read()
        env = Environment(
            loader=DictLoader(dict(template=template_source)),
            autoescape=select_autoescape(default=False)
        )
        template = env.get_template("template")
        report = template.render(**config["template_variables"])
        # Create report object including report
        report_name = config["report_name"]
        reports_path = config["reports_path"]
        workspace_name = config["workspace_name"]
        os.makedirs(reports_path, exist_ok=True)
        report_path = os.path.join(reports_path, "index.html")
        with open(report_path, "w") as report_file:
            report_file.write(report)
        html_links = [
            {
                "description": "report",
                "name": "index.html",
                "path": reports_path,
            },
        ]
        report_info = self.report.create_extended_report(
            {
                "direct_html_link_index": 0,
                "html_links": html_links,
                "message": "A sample report.",
                "report_object_name": report_name,
                "workspace_name": workspace_name,
            }
        )
        return {
            "report_name": report_info["name"],
            "report_ref": report_info["ref"],
        }

    def do_analysis(self, params:dict):
        self.validate_do_analysis(params)
        report_info = self.clients.KBaseReport.create({
            'report': {
                'objects_created': [],
                'text_message': params['param_1']
            },
            'workspace_name': params['workspace_name']
        })
        return {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }

    def validate_do_analysis(self, params:dict):
        param_1 = params.get("param_1")
        if not isinstance(param_1, str):
            raise Exception("Please provide a string for param_1.")

        param_2 = params.get("param_2")
        if not isinstance(param_2, list):
            raise Exception("Please provide a list for param_2.")

        param_3 = params.get("param_3")
        if not isinstance(param_3, dict):
            raise Exception("Please provide a dict for param_3.")

        param_4 = params.get("param_4")
        if not (0 < param_4 < 100):
            raise Exception(
                "Please provide a between 0 and 100 for param_4"
            )
