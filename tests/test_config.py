from unittest import TestCase


class TestConfig(TestCase):
    def test_read_config(self):
        try:
            import src.svo_log_api.config
        except Exception as err:
            self.fail(f'Import config raised exception: {err.__class__.__name__}{err.args}')
