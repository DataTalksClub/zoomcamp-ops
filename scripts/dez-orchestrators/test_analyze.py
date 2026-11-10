import unittest
from analyze import detect, repo_name

class DetectionTests(unittest.TestCase):
    def test_url_normalization(self):
        self.assertEqual(repo_name('https://github.com/Owner/project.git/tree/main/final'), 'Owner/project')
        self.assertEqual(repo_name('https://evil.example/Owner/project'), '')
        self.assertEqual(repo_name('https://github.com/Owner'), '')

    def test_executable_multi_tool(self):
        ev,_,_=detect([('dags/job.py','from airflow import DAG'),('flows/job.yml','id: pipeline\nnamespace: final\ntasks:\n - type: io.kestra.plugin.core.log.Log'),('Dockerfile','FROM quay.io/astronomer/astro-runtime:12')])
        self.assertEqual(set(ev), {'Airflow','Astronomer','Kestra'})

    def test_notes_are_not_use(self):
        ev,weak,_=detect([('README.md','We studied Airflow, Prefect and Kestra.'),('homework/dags/test.py','from airflow import DAG')])
        self.assertFalse(ev)
        self.assertTrue(weak)

    def test_other_orchestrators(self):
        ev,_,_=detect([('pipeline.py','from prefect import flow\nfrom dagster import asset\nimport luigi'),('mage/metadata.yaml','blocks: []\nexecutor_type: local_python')])
        self.assertEqual(set(ev),{'Prefect','Dagster','Luigi','Mage'})

    def test_tools_not_orchestrators(self):
        ev,_,_=detect([('requirements.txt','dbt-core\ndlt\npyspark\n'),('analysis.py','import pandas\n')])
        self.assertFalse(ev)

if __name__ == '__main__': unittest.main()
