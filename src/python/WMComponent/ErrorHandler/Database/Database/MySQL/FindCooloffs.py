#!/usr/bin/env python
#pylint: disable-msg=E1103

"""
_FindCooloffs_

This module implements the mysql backend for the 
retry manager, for locating the jobs in cooloff state state

"""

__revision__ = \
    "$Id: FindCooloffs.py,v 1.1 2009/05/12 16:39:45 afaq Exp $"
__version__ = \
    "$Revision: 1.1 $"
__author__ = \
    "anzar@fnal.gov"

import threading

from WMCore.Database.DBFormatter import DBFormatter

class FindCooloffs(DBFormatter):
    """
    This module implements the mysql backend for the retry manager, 
	for locating the jobs in cooloff state state
 
    """
    
    sqlStr = """SELECT wmbs_job.id as ID, jsm_state.retry_max as RETRY_MAX, wmbs_job.retry_count as RETRY_COUNT 
			FROM wmbs_job, jsm_state WHERE wmbs_job.status = :job_status and jsm_state.ID=wmbs_job.state  limit 100"""
    
    def __init__(self):
        myThread = threading.currentThread()
        DBFormatter.__init__(self, myThread.logger, myThread.dbi)
    
    def getBinds(self, jobStatus):
        print dataset
        binds =  { 'job_status': jobStatus}
        return binds
   
    def formatDict(self, result):
        """
        _formatDict_

        Cast the id, jobgroup and last_update columns to integers because
        formatDict() turns everything into strings.
        """
        formattedResult = DBFormatter.formatDict(self, result)[0]
        formattedResult["id"] = int(formattedResult["id"])
        formattedResult["retry_count"] = int(formattedResult["retry_count"])
        formattedResult["retry_max"] = int(formattedResult["retry_max"])
        return formattedResult
 
    def execute(self, jobStatus, conn=None, transaction = False):
        binds = self.getBinds(jobStatus)
        result = self.dbi.processData(self.sql, binds,
                         conn = conn, transaction = transaction)
        return result

