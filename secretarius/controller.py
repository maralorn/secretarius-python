import psycopg2, psycopg2.extras
import getpass


class Controller():
    def __init__(self, user=getpass.getuser()):

        self.__auth = "host=localhost dbname=pim user=%s" % (user,)

    def _open(self):
        self.__conn = psycopg2.connect(self.__auth)
        self.__cursor = self.__conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.exc = self.__cursor.execute
        self.one = self.__cursor.fetchone
        self.all = self.__cursor.fetchall

    def new_information(self, inbox=True, urgent=False):
        self.exc("INSERT INTO information (inbox, urgent) VALUES (%s,%s) RETURNING id;",(inbox, urgent))
        return self.one()['id']
    
    def create_appointment(self, description, date, time=None, length=None, referencing=None):
        id = self.new_information(False, False)
        self.exc("INSERT INTO appointment (id, description, date, time, length) VALUES (%s, %s, %s, %s, %s)", (id, description, date, time, length))
        if referencing:
            self.new_reference(id, referencing)
        return id

    def new_task(self, description):
        id = self.new_information(False, False)
        self.exc("INSERT INTO task (id, description) VALUES (%s, %s);", (id, description))
        return id

    def new_file(self, name):
        self.exc("INSERT INTO file (name) VALUES (%s) RETURNING id;",(name,))
        return self.one()["id"]

    def delete_info(self, _id):
        self.exc("DELETE FROM information WHERE id= %s",(_id,))

    def get_note(self, _id):
        return self.get_information(_id, "note")

    def maybe_info(self, _id):
        self.exc("UPDATE information SET inbox=FALSE, urgent=FALSE, maybe=TRUE WHERE id=%s",(_id,))

    def archive_info(self, _id):
        self.exc("UPDATE information SET inbox=FALSE, urgent=FALSE, maybe=FALSE WHERE id=%s",(_id,))

    def delay_info(self, _id, until):
        self.exc("UPDATE information SET inbox=FALSE, urgent=FALSE, maybe=FALSE, delay=%s WHERE id=%s",(until, _id))

    def new_note(self, content, attachment=None):
        id = self.new_information()
        self.exc("INSERT INTO note (id, content, attachment) VALUES (%s, %s, %s);",(id, content, attachment))
        return id

    def new_reference(self, id, referencing):
        self.exc('INSERT INTO "references" (id, referenceid) VALUES (%s, %s);', (id, referencing))

    def create_project(self, description, referencing=None, parent=None):
        id = self.new_task(description)
        self.exc("INSERT INTO project (id, parent) VALUES (%s, %s);",(id, parent))
        if referencing:
            self.new_reference(id, referencing)
        return id

    def create_asap(self, description, list, referencing=None, project=None):
        id = self.new_task(description)
        self.exc("INSERT INTO asap (id, asaplist, project) VALUES (%s, (SELECT id FROM asaplist WHERE name=%s), %s);",(id, list, project))
        if referencing:
            self.new_reference(id, referencing)
        return id
    
    def project_set_parent(self, id, parent):
        self.exc("UPDATE project SET parent=%s WHERE id=%s;",(parent, id))
    
    def asap_set_project(self, id, project):
        self.exc("UPDATE asap SET project=%s WHERE id=%s;",(project, id))
        
        
    def create_asaplist(self, name):
        self.exc("INSERT INTO asaplist (name) VALUES (%s)", (name,))
        
    def asaplist_get_names(self):
        self.exc("SELECT name FROM asaplist;")
        return self.all()
    
    def change_asaplist(self, id, list):
        self.exc("UPDATE asap AS a SET asaplist=l.id FROM asaplist l WHERE l.name=%s AND a.id=%s", (list, id))

    def rename_asaplist(self, name, new_name):
        self.exc("UPDATE asaplist SET name=%s WHERE name=%s", (new_name, name))
        
    def asaplist_delete(self, name):
        self.exc("DELETE FROM asaplist WHERE name=%s", (name,))
    
    def asaplist_get(self, name):
        self.exc("SELECT a.* FROM asapview a WHERE a.asaplist = %s AND completed IS NULL", (name,))
        return self.all()
    
    def asap_get_all(self):
        self.exc("SELECT * FROM asapview WHERE completed IS NULL")
        return self.all()

    def project_get_all(self):
        self.exc("SELECT * FROM projectview WHERE completed IS NULL")
        return self.all()

    def get_type(self, id):
        self.exc("SELECT type FROM type WHERE id=%s;", (id,))
        return self.one()["type"]

    def get_filename(self, id):
        self.exc("SELECT name FROM file WHERE id=%s;", (id,))
        try:
            return self.one()["name"]
        except:
            raise ValueError("File ID not found.")

    def get_information(self, _id, _type=None):
        if not _type:
            _type = self.get_type(_id)
        self.exc("SELECT * FROM " + _type + "view WHERE id=%s;" , (_id,))
        return self.one()
    
    def later_get_list(self):
        self.exc("SELECT later.*, type FROM type, later WHERE type.id=later.id ORDER BY last_edited;")
        return self.all()
        
    def first_in_inbox(self):
        self.exc("SELECT inbox.id, type FROM type, inbox WHERE type.id=inbox.id ORDER BY created_at LIMIT 1;")
        ret = self.one()
        if ret:
            return self.get_information(ret["id"], ret["type"])
        else:
            return None
    
    def change_note(self, id, content):
        self.exc("UPDATE note SET content=%s WHERE id=%s;", (content, id))
    
    def note_delete_attachment(self, id):
        self.exc("UPDATE note SET attachment=%s WHERE id=%s;", (None, id))
    
    def info_remove_reference(self, id, referenceid):
        self.exc("DELETE FROM references WHERE id=%s AND referenceid=%s", (id, referenceid))

    def count_inbox(self):
        self.exc("SELECT count(*) FROM inbox;")
        return int(self.one()["count"])

    def count_urgent(self):
        self.exc("SELECT count(*) FROM inbox WHERE urgent=TRUE;")
        return int(self.one()["count"])

    def task_done(self, id):
        self.exc("UPDATE task SET completed=CURRENT_TIMESTAMP WHERE id=%s", (id,))

    def _close(self):
        self.__conn.commit()
        self.__cursor.close()
        self.__conn.close()
