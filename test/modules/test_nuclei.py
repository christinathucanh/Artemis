from test.base import ArtemisModuleTestCase

from karton.core import Task

from artemis.binds import TaskStatus, TaskType
from artemis.modules.nuclei import Nuclei


class NucleiTest(ArtemisModuleTestCase):
    # The reason for ignoring mypy error is https://github.com/CERT-Polska/karton/issues/201
    karton_class = Nuclei  # type: ignore

    def test_simple(self) -> None:
        task = Task(
            {"type": TaskType.URL.value},
            payload={
                "url": "http://test-phpmyadmin-easy-password/",
                "content": '(...)<img src="./themes/pmahomme/img/logo_right.png" id="imLogo" name="imLogo" alt="phpMyAdmin" border="0">',
            },
        )
        self.run_task(task)
        (call,) = self.mock_db.save_task_result.call_args_list
        self.assertEqual(call.kwargs["status"], TaskStatus.INTERESTING)
        self.assertEqual(
            call.kwargs["status_reason"],
            "[high] phpMyAdmin Default Login phpMyAdmin default admin credentials were discovered",
        )