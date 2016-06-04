#!/usr/bin/env python
"""
Migrate data from WTS to PWTS

NOTE: must source ../Configuration before use
"""
import psycopg2
import argparse


def parseArgs():
    """
    Return script arguments
    """
    parser = argparse.ArgumentParser(description='Migrate WTS data to PWTS database')
    parser.add_argument('source_wts_server', help='wts server')
    parser.add_argument('source_wts_db', help='wts dbname')
    parser.add_argument('target_server', help='pwts server')
    parser.add_argument('target_pwts_db', help='pwts dbname')
    parser.add_argument('-k','--key', nargs="?", help='migrate single _tr_key')

    args = parser.parse_args()
    return args
    

def loadRecords(rows, tableName, cursor):
    """
    Load rows in pwts.tableName
    using target db cursor
    """
    
    if not rows:
            return
    
    # create a format string for all the rows
    # i.e. (%s,%s,%s,%s,...)
    formatArgs = []
    for i in range(len(rows[0])):
            formatArgs.append("%s")
            
    valueTemplate = "(%s)" % (",".join(formatArgs))
    
    # bulk insert using execute
    argsStr = ','.join(cursor.mogrify(valueTemplate, x) for x in rows)
    cursor.execute("INSERT INTO " + tableName + " VALUES " + argsStr) 


def migrateWTS(
    source_server,
    source_dbname,
    target_server,
    target_dbname,
    _tr_key = None
    ):
    """
    Migrates data from source_server:source_dbname
	to target_server:target_dbname
    
    Optional: migrate only one _tr_key
    """

    print "source server = %s" % source_server
    print "source dbname = %s" % source_dbname
    print "target server = %s" % target_server
    print "target dbname = %s" % target_dbname
    if _tr_key:
        print "_tr_key = %s" % _tr_key
        
        
    sourceConn = psycopg2.connect("host='%s' dbname='%s' user='mgd_public'" % 
                                   (source_server,
                                   source_dbname))
    sourceCur = sourceConn.cursor()
    
    targetConn =  psycopg2.connect("host='%s' dbname='%s' user='mgd_dbo'" % 
                                   (target_server,
                                   target_dbname))
    targCur = targetConn.cursor()
    
    migrate_controlled_vocabs(sourceCur, targCur)
    
    if _tr_key:
            migrate_trackrecords(sourceCur, targCur, _tr_key=_tr_key)
            migrate_assocs(sourceCur,targCur, _tr_key=_tr_key)
            migrate_status_history(sourceCur,targCur, _tr_key=_tr_key)
    else:
            migrate_trackrecords(sourceCur, targCur)
            migrate_assocs(sourceCur, targCur)
            migrate_status_history(sourceCur,targCur)
    
    
    targetConn.commit()
    
    
    
def migrate_controlled_vocabs(sourceCur, targCur):
        """
        migrate all cv_* tables
        """
        
        # staff table
        
        sourceCur.execute("""
          select _staff_key, staff_username, active
          from cv_staff
        """)
        
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                row[2] = bool(row[2])
                rows.append(row)
        
        loadRecords(rows, "cv_user", targCur)
        
        # area table
        sourceCur.execute("""
          select _area_key, area_name, area_description, active
          from cv_wts_area
        """)
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                row[3] = bool(row[3])
                rows.append(row)
        
        loadRecords(rows, "cv_wts_area", targCur)
        
        # size table
        sourceCur.execute("""
          select _size_key, size_name, size_description, active
          from cv_wts_size
        """)
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                row[3] = bool(row[3])
                rows.append(row)
        
        loadRecords(rows, "cv_wts_size", targCur)
        
        # status table
        sourceCur.execute("""
          select _status_key, status_name, status_description, active
          from cv_wts_status
        """)
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                row[3] = bool(row[3])
                rows.append(row)
        
        loadRecords(rows, "cv_wts_status", targCur)
        
        # type table
        sourceCur.execute("""
          select _type_key, type_name, type_description, active
          from cv_wts_type
        """)
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                row[3] = bool(row[3])
                rows.append(row)
        
        loadRecords(rows, "cv_wts_type", targCur)
        
        # priority table
        sourceCur.execute("""
          select _priority_key, priority_name, priority_description, active
          from cv_wts_priority
        """)
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                row[3] = bool(row[3])
                rows.append(row)
        
        loadRecords(rows, "cv_wts_priority", targCur)
        
        # category table
        sourceCur.execute("""
          select _category_key, category_name, category_description, active,
          category_email, _area_key, _type_key, _status_key
          from cv_wts_category
        """)
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                row[3] = bool(row[3])
                rows.append(row)
        
        loadRecords(rows, "cv_wts_category", targCur)


def migrate_trackrecords(sourceCur, targCur, _tr_key=None):
        """
        migrate core wts_trackrec table
        
        Optional migrate only one _tr_key
        """
        
        # trackrec table
        q = """
         select tr._tr_key, 
           _priority_key,
           _size_key,
           _status_key,
           _status_staff_key,
           status_set_date,
           _locked_staff_key,
           locked_when,
           tr_title,
           directory_variable,
           attention_by,
           creation_date,
           modification_date,
           tr_d.text_block as description,
           tr_pn.text_block as progress_notes
          from wts_trackrec tr
          left outer join wts_text tr_d
                  on tr_d._tr_key = tr._tr_key
                  and tr_d.text_type = 2
          left outer join wts_text tr_pn
                  on tr_pn._tr_key = tr._tr_key
                  and tr_pn.text_type = 3
        """
        if _tr_key:
                q += " where tr._tr_key = %s" % _tr_key
        
        sourceCur.execute(q)
        
        rows = []
        for row in sourceCur.fetchall():
                row = list(row)
                # title
                row[8] = row[8].decode('iso-8859-1')
                
                # convert directory variable to flag
                row[9] = bool(row[9]) 
                # description and progress notes blocks
                if row[13]:
                        row[13] = row[13].decode('iso-8859-1')
                if row[14]:
                        row[14] = row[14].decode('iso-8859-1')
                rows.append(row)
        
        loadRecords(rows, "wts_trackrec", targCur)
        
        
def migrate_assocs(sourceCur, targCur, _tr_key=None):
        """
        migrate wts_trackrec associations
        
        Optional migrate only one _tr_key
        """
        
        # TR areas
        q = """
         select _tr_key, _area_key
         from wts_area
        """
        if _tr_key:
                q += " where _tr_key = %s" % _tr_key
        
        sourceCur.execute(q)
        
        loadRecords(sourceCur.fetchall(), "wts_tr_area", targCur)
        
        # TR areas
        q = """
         select _tr_key, _type_key
         from wts_type
        """
        if _tr_key:
                q += " where _tr_key = %s" % _tr_key
        
        sourceCur.execute(q)
        
        loadRecords(sourceCur.fetchall(), "wts_tr_type", targCur)
        
        # TR assigned staff
        q = """
         select _tr_key, _staff_key
         from wts_staff_assignment
        """
        if _tr_key:
                q += " where _tr_key = %s" % _tr_key
        
        sourceCur.execute(q)
        
        loadRecords(sourceCur.fetchall(), "wts_tr_assign_user", targCur)
        
        # TR requested by staff
        q = """
         select _tr_key, _staff_key
         from wts_requested_by
        """
        if _tr_key:
                q += " where _tr_key = %s" % _tr_key
        
        sourceCur.execute(q)
        
        loadRecords(sourceCur.fetchall(), "wts_tr_request_user", targCur)
        
        if not _tr_key:
            # TR relationships
     
            sourceCur.execute("""
              select _tr_key,
               _related_tr_key,
               transitive_closure
              from wts_relationship
            """)
            
            rows = []
            for row in sourceCur.fetchall():
                    row = list(row)
                    row[2] = bool(row[2])
                    rows.append(row)

            loadRecords(rows, "wts_relationship", targCur)
        

def migrate_status_history(sourceCur, targCur, _tr_key=None):
        """
        migrate wts_trackrec status change history
        
        Optional migrate only one _tr_key
        """
        
        # TR status history
        q = """
         select _tr_key, 
         _status_key,
         _staff_key,
         set_date
         from wts_status_history
        """
        if _tr_key:
                q += " where _tr_key = %s" % _tr_key
        
        sourceCur.execute(q)
        
        rows = []
        uniqueKey = 1
        for row in sourceCur.fetchall():
                row = list(row)
                # add unique key
                row.insert(0, uniqueKey)
                uniqueKey += 1
                
                rows.append(row)
        
        loadRecords(rows, "wts_status_history", targCur)



if __name__ == "__main__":
    args = parseArgs() 

    migrateWTS(
      source_server=args.source_wts_server,
      source_dbname=args.source_wts_db,
      target_server=args.target_server,
      target_dbname=args.target_pwts_db,
      _tr_key = args.key
    )
