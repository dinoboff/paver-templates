"""
Paver-enable template

Copyright (c) 2009, Damien Lebrun
All rights reserved.


Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from datetime import date
import shutil
import os
import ConfigParser

from paste.script.templates import Template, var
from setuptools.command.setopt import edit_config, config_file
from pkg_resources import resource_filename

__author__ = 'Damien Lebrun <dinoboff@hotmail.com>'

YEAR = date.today().year

LICENSE_HEADER = """%(description)s

Copyright (c) %(year)s, %(author)s
All rights reserved.

"""

GPL = """
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU%(gpl_type)s General Public License as published by
the Free Software Foundation, either version %(gpl_version)s of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU%(gpl_type)s General Public License for more details.

You should have received a copy of the GNU%(gpl_type)s General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

BSD = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

    * Neither the name of the %(org)s nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

FREE_BSD = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


def add_license_details(vars):
    """Populates ``vars`` with ``gpl_type``, ``gpl_version``, 
    ``license_body`` and ``license_files``.
    """
    vars.setdefault('description', '')
    vars.setdefault('author', '')
    vars.setdefault('author_email', '')
    vars.setdefault('license_name', '')
    vars['gpl_type'] = ''
    vars['gpl_version'] = ''
    vars['license_files'] = []
    license_tmpl = ''
    license = vars.get('license_name', '').strip().upper()
    if license:
        if license == 'BSD':
            if vars.get('org'):
                license_tmpl = BSD
            else:
                license_tmpl = FREE_BSD
        elif 'GPL' in license:
            license_tmpl = GPL
            if license == 'GPLV2':
                vars.update(gpl_version=2, license_files=('gpl-2.0',))
            elif license in ('LGPL', 'LGPLV3',):
                vars.update(
                    gpl_version=3,
                    gpl_type=' Lesser',
                    license_files=('gpl', 'lgpl',))
            elif license == 'LGPLV2':
                vars.update(
                    gpl_version=2,
                    gpl_type=' Lesser',
                    license_files=('gpl-2.0', 'lgpl-2.1',))    
            elif license in ('AGPL', 'AGPLV3',):
                vars.update(
                    gpl_version=3,
                    gpl_type=' Affero',
                    license_files=('gpl', 'agpl',))
            else:
                vars.update(gpl_version=3, license_files=('gpl',))
    vars['license_body'] = (LICENSE_HEADER + license_tmpl) % vars
    
def copy_license(license_files, output_dir):
    """copy gpl license files to output directory"""
    for file_name in license_files:
        full_name = '%s.txt' % file_name
        rel_path = 'paster-templates/licenses/%s' % full_name
        abs_path = resource_filename(__name__, rel_path)
        shutil.copyfile(abs_path, os.path.join(output_dir, full_name))

def get_default():
    """Get default author name and email to use for new package"""
    config_path = config_file('user')
    cp = ConfigParser.RawConfigParser()
    cp.read(config_path)
    defaults=[]
    for option in ('author', 'author_email'):
        try:
            defaults.append(cp.get('paver', 'default.%s' % option))
        except (ConfigParser.NoSectionError, ConfigParser.NoSectionError,):
            defaults.append('')
    return defaults

def save_defaults(**kw):
    """Save in ~/.pydistutils the author name and email.
    
    To be used as default value for the next use of this template."""
    options = {}
    for option in ('author','author_email'):
        value = kw.get(option, '')
        if value:
            options['default.%s' % option] = value
    edit_config(config_file('user'), {'paver': options})

DEFAULT_NAME, DEFAULT_EMAIL = get_default()


class PaverTemplate(Template):
    _template_dir = 'paster-templates/paver_package'
    summary = "A basic paver-enabled package"
    use_cheetah = True
    vars = [
        var('version', 'Version (like 0.1)'),
        var('description', 'One-line description of the package'),
        var('keywords', 'Space-separated keywords/tags'),
        var('author', 'Author name', default=DEFAULT_NAME),
        var('author_email', 'Author email', default=DEFAULT_EMAIL),
        var('url', 'URL of homepage'),
        var('license_name',
            'license name - GPLv2/GPLv3/LGPLv2/LGPLv3/AGPLv3/BSD/...',
            default='BSD'),
        var('org', 'Organisation name (required for 3-clause BSD).'),
        ]
    
    def pre(self, command, output_dir, vars):
        """
        Set extra template variables:
        
        * "year", current year.
        * "license_body", license notice of the package.
        * "gpl_type", for gpl licenses
        """
        vars['year'] = YEAR 
        add_license_details(vars)
    
    def post(self, command, output_dir, vars):
        """Save the author, author_name and org variables in ~/.pydistutils.cfg,
        And copy the gpl license if necessary."""
        save_defaults(**vars)
        copy_license(vars['license_files'], output_dir)