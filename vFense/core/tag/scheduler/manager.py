from vFense.core.operations._constants import AgentOperations
from vFense.core.scheduler import Schedule
from vFense.core.scheduler._constants import (
    ScheduleKeys, ScheduleTriggers
)
from vFense.core.scheduler.decorators import update_job_history
from vFense.core.scheduler.manager import JobManager
from vFense.core.tag._db import fetch_tags_by_view
from vFense.core.agent.operations.store_agent_operations import (
    StoreAgentOperations
)

@update_job_history
def reboot_tags(tag_ids=None, view_name=None, user_name=None):
    """Reboot tags
    Kwargs:
        tag_ids (list): List of tag ids.
        view_name (str): The name of the view, this operation is being
            performed on.
        user_name (str): The user who performed this operation.
    """
    operation = StoreAgentOperations(user_name, view_name)
    if not tag_ids:
        tag_ids = fetch_tags_by_view(view_name=view_name)

    for tag_id in tag_ids:
        operation.reboot(tag_id=tag_id)


class TagJobManager(JobManager):
    def reboot_once(self, start_date, label,
                    user_name, agents=None, time_zone=None):
        """Reboot 1 or multiple agents once.
        Args:
            start_date (float): The unix time, aka epoch time
            label (str): The name of this job.
            user_name (str): The name of the use who initiated this job.

        Kwargs:
            agents (list): List of agent ids.
            time_zone (str):  Example... UTC, Chile/EasterIsland
        """
        job_kwargs = {
            ScheduleKeys.Agents: agents,
            ScheduleKeys.UserName: user_name,
            ScheduleKeys.ViewName: self.view_name,
        }
        job = (
            Schedule(
                label, reboot_agents, job_kwargs, run_date=start_date,
                operation=AgentOperations.REBOOT, time_zone=time_zone,
                trigger=ScheduleTriggers.DATE
            )
        )
        results = self.add_date_job(job)
        return results

    def reboot_cron(self, start_date, label,
                    user_name, agents=None, time_zone=None):
        """Reboot 1 or multiple agents on an interval.
        Args:
            start_date (float): The unix time, aka epoch time
            label (str): The name of this job.
            user_name (str): The name of the use who initiated this job.

        Kwargs:
            agents (list): List of agent ids.
            time_zone (str):  Example... UTC, Chile/EasterIsland
        """
        job_kwargs = {
            ScheduleKeys.Agents: agents,
            ScheduleKeys.UserName: user_name,
            ScheduleKeys.ViewName: self.view_name,
        }
        job = (
            Schedule(
                label, reboot_agents, job_kwargs, start_date,
                operation=AgentOperations.REBOOT, time_zone=time_zone,
                trigger=ScheduleTriggers.DATE
            )
        )
        results = self.add_cron_job(job)
        return results