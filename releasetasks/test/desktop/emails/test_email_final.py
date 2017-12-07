import unittest

from releasetasks.test.desktop import make_task_graph, do_common_assertions, \
    get_task_by_name, create_firefox_test_args
from releasetasks.test import PVT_KEY_FILE, verify
from voluptuous import Schema, truth


class TestEmailFinal(unittest.TestCase):
    maxDiff = 30000
    graph = None
    task = None
    payload = None

    def setUp(self):
        self.task_schema = Schema({
            'task': {
                'provisionerId': 'aws-provisioner-v1',
                'workerType': 'gecko-3-decision',
                'payload': {
                    'command': ['/bin/echo', 'Dummy task to tell pulse-notify to send an email'],
                },
                'metadata': {
                    'name': 'firefox email release-drivers foo',
                },
                'extra': {
                    'notifications': {
                        'task-completed': {
                            'subject': 'firefox foo 42.0b2 updates ready for sign-off on foo channel now',
                            'message': '\n'.join([
                                'firefox foo 42.0b2 updates ready for sign-off on foo channel now',
                                '',
                                'Scheduled changes can be approved at https://aus4-admin.mozilla.org/rules?product=Firefox&channel=foo',
                            ]),
                            'ids': ['release-drivers'],
                        },
                    },
                },
            },
        }, extra=True, required=True)

        test_kwargs = create_firefox_test_args({
            'push_to_candidates_enabled': True,
            'push_to_releases_enabled': True,
            'signing_pvt_key': PVT_KEY_FILE,
            'release_channels': ['foo'],
            'final_verify_channels': ['foo'],
            'publish_to_balrog_channels': ["release-dev", "alpha"],
            'accepted_mar_channel_id': 'firefox-mozilla-beta',
            'signing_cert': 'dep',
            'moz_disable_mar_cert_verification': True,
            'en_US_config': {
                "platforms": {
                    "macosx64": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                    "win32": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                    "win64": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                    "linux": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc'},
                    "linux64": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                }
            },
        })

        self.graph = make_task_graph(**test_kwargs)
        self.task = get_task_by_name(self.graph, "release-foo-firefox_email_foo")

    def generate_task_requires_validator(self):
        requires_sorted = sorted([get_task_by_name(self.graph, "release-foo-firefox_schedule_publishing_in_balrog")["taskId"]])

        @truth
        def validate_task_requires(task):
            return sorted(task['requires']) == requires_sorted

        return validate_task_requires

    def test_email_final(self):
        verify(self.task, self.task_schema, self.generate_task_requires_validator())

    def test_common_assertions(self):
        do_common_assertions(self.graph)


class TestEmailFinalTwoChannels(unittest.TestCase):
    maxDiff = 30000
    graph = None
    task = None
    payload = None

    def setUp(self):
        self.task_schema = Schema({
            'task': {
                'provisionerId': 'aws-provisioner-v1',
                'workerType': 'gecko-3-decision',
                'payload': {
                    'command': ['/bin/echo', 'Dummy task to tell pulse-notify to send an email'],
                },
                'metadata': {
                    'name': 'firefox email release-drivers beta',
                },
                'extra': {
                    'notifications': {
                        'task-completed': {
                            'subject': 'firefox beta 42.0b2 updates ready for sign-off on beta channel now',
                            'message': '\n'.join([
                                'firefox beta 42.0b2 updates ready for sign-off on beta channel now',
                                '',
                                'Scheduled changes can be approved at https://aus4-admin.mozilla.org/rules?product=Firefox&channel=beta',
                            ]),
                            'ids': ['release-drivers'],
                        },
                    },
                },
            },
        }, extra=True, required=True)

        test_kwargs = create_firefox_test_args({
            'push_to_candidates_enabled': True,
            'push_to_releases_enabled': True,
            'signing_pvt_key': PVT_KEY_FILE,
            'release_channels': ['beta', 'release'],
            'final_verify_channels': ['beta'],
            'publish_to_balrog_channels': ["release-dev", "alpha"],
            'accepted_mar_channel_id': 'firefox-mozilla-beta',
            'signing_cert': 'dep',
            'moz_disable_mar_cert_verification': True,
            'en_US_config': {
                "platforms": {
                    "macosx64": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                    "win32": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                    "win64": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                    "linux": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc'},
                    "linux64": {'signed_task_id': 'abc', 'unsigned_task_id': 'abc', "ci_system": "tc"},
                }
            },
        })

        self.graph = make_task_graph(**test_kwargs)
        self.task = get_task_by_name(self.graph, "release-foo-firefox_email_beta")

    def generate_task_requires_validator(self):
        requires_sorted = sorted([get_task_by_name(self.graph, "release-foo-firefox_schedule_publishing_in_balrog")["taskId"]])

        @truth
        def validate_task_requires(task):
            return sorted(task['requires']) == requires_sorted

        return validate_task_requires

    def test_email_final(self):
        verify(self.task, self.task_schema, self.generate_task_requires_validator())

    def test_common_assertions(self):
        do_common_assertions(self.graph)
