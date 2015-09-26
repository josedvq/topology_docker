# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP <asicapi@hp.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Module to determine root / non-root and define the prefix required for
commands.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging
from os import getuid, devnull
from subprocess import call
from shlex import split as shsplit


log = logging.getLogger(__name__)


def cmd_prefix():
    if hasattr(cmd_prefix, 'prefix'):
        return cmd_prefix.prefix

    if getuid() == 0:
        cmd_prefix.prefix = ''
        return cmd_prefix.prefix

    with open(devnull, 'w') as f:
        cmd = shsplit('sudo --non-interactive ip --help')
        if call(cmd, stdout=f, stderr=f) != 0:
            raise RuntimeError(
                'Please configure the ip command for root execution'
            )

    cmd_prefix.prefix = 'sudo --non-interactive '
    return cmd_prefix.prefix