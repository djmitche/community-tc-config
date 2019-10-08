# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import jsone

from tcadmin.resources import Role


repo_access = [
    {
        'scopes': [
        ],
        'worker-pools': [
            'proj-taskcluster/ci',
        ],
        'for': [
            'github.com/taskcluster/*',
        ]
    },
]


async def update_resources(resources):
    resources.manage('Role=repo:.*')
    by_role = {}

    for ra in repo_access:
        roles = ['repo:' + r for r in ra['for']]
        scopes = (
            ra.get('scopes', []) +
            ['queue:create-task:highest:' + wp for wp in ra.get('worker-pools', [])]
        )
        for role_id in roles:
            by_role.setdefault(role_id, set()).update(scopes)

    for role_id, scopes in by_role.items():
        resources.add(Role(
            roleId=role_id,
            description='',
            scopes=list(scopes)))
