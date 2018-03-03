# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from dockerizer.builders.jobs import BaseJobDockerBuilder, build_job
from projects.models import Project

logger = logging.getLogger('polyaxon.dockerizer.builders')


class NotebookDockerBuilder(BaseJobDockerBuilder):
    def _check_pulse(self, check_pulse):
        # Check if experiment is not stopped in the meanwhile
        if check_pulse > self.CHECK_INTERVAL:
            try:
                project = Project.objects.get(id=self.project_id)
            except Project.DoesNotExist:
                logger.info('Project `{}` does not exist anymore, stopping build'.format(
                    self.project_name))
                return check_pulse, True

            if not project.has_notebook or not project.notebook:
                logger.info('Project `{}` does not have a notebook anymore, stopping build'.format(
                    self.project_name))
                return check_pulse, True
            else:
                check_pulse = 0
        return check_pulse, False


def build_notebook_job(project, job):
    return build_job(project=project, job=job, job_builder=NotebookDockerBuilder)