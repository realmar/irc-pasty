#!/usr/bin/env python3

import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = 'templates'
TEMPLATE_DIR_SAVE = 'tests_js/mock/templates'
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class PastyTemplate:
    def __init__(self, env, template, **kwargs):
        self.template = template
        self.variables = kwargs
        self.env = env
    
    def buildTemplate(self):
        t = env.get_template(self.template)
        self.render = t.render(self.variables)
        return self
    
    def saveTemplate(self, location):
        if self.render == None:
            return
        
        file = open(location, 'w')
        file.write(self.render)

templates = [
    PastyTemplate(env, 'post.html', irc={'channels' : []}),
    PastyTemplate(env, 'all.html')
    ]

for t in templates:
    t.buildTemplate().saveTemplate(os.path.join(TEMPLATE_DIR_SAVE, t.template))