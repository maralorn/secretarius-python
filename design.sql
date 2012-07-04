
-- +information
-- |-note
-- |+task
--  |-project
--  |-asap
-- |-appointment
-- |+social_entity
--  |-circle
--  |-contact
-- |-place



CREATE TABLE information(
	inbox		boolean DEFAULT FALSE NOT NULL,
	urgent		boolean DEFAULT FALSE NOT NULL,
	maybe		boolean DEFAULT FALSE NOT NULL,
	delay		timestamp,
	last_edited timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	created_at 	timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	id 			serial PRIMARY KEY
);

--DROP TABLE file CASCADE;
CREATE TABLE "file"(
	id 			serial PRIMARY KEY,
	name		varchar NOT NULL	
);

CREATE TABLE note(
	content 	varchar NOT NULL,
	id			integer PRIMARY KEY REFERENCES information(id) ON DELETE CASCADE,
	attachment 	integer REFERENCES "file"(id) ON DELETE RESTRICT
);

CREATE TABLE task(
	description varchar NOT NULL,
	completed 	timestamp,
	id 			integer PRIMARY KEY REFERENCES information(id) ON DELETE CASCADE
);

CREATE TABLE "references"(
	id			integer REFERENCES information(id) ON DELETE CASCADE,
	referenceid	integer REFERENCES information(id) ON DELETE CASCADE,
	PRIMARY KEY (id, referenceid)
);

CREATE TABLE project(
	parent 		integer REFERENCES project(id),
	id			integer PRIMARY KEY REFERENCES task(id) ON DELETE CASCADE
);

--DROP TABLE asaplist CASCADE;
CREATE TABLE asaplist(
	id 			serial PRIMARY KEY,
	name 		varchar NOT NULL UNIQUE
);

--DROP TABLE asap CASCADE;
CREATE TABLE asap(
	project 	integer REFERENCES project(id),
	asaplist 	integer REFERENCES asaplist(id) ON DELETE RESTRICT NOT NULL,
	id 			integer PRIMARY KEY REFERENCES task(id) ON DELETE CASCADE
);

CREATE TABLE social_entity(
	id 			integer PRIMARY KEY REFERENCES information(id) ON DELETE CASCADE
);

--DROP TABLE circle CASCADE;
CREATE TABLE circle(
	id 			integer PRIMARY KEY REFERENCES social_entity(id) ON DELETE CASCADE,
	name 		varchar	NOT NULL UNIQUE
);

CREATE TABLE contact(
	id 			integer PRIMARY KEY REFERENCES social_entity(id) ON DELETE CASCADE
);

CREATE TABLE place(
	id 			integer PRIMARY KEY REFERENCES information(id) ON DELETE CASCADE
);


CREATE TABLE appointment(
	id 			integer PRIMARY KEY REFERENCES information(id) ON DELETE CASCADE,
	"date"		date 	NOT NULL,
	time		time,
	length 		interval,
	description	varchar NOT NULL,
	place		integer REFERENCES place(id)
);

CREATE TABLE participants(
	appointmentid integer REFERENCES appointment(id) ON DELETE CASCADE,
	participantid integer REFERENCES social_entity(id) ON DELETE CASCADE,
	PRIMARY KEY (appointmentid, participantid)
);

--
-- +information
-- |-note
-- |+task
--  |-project
--  |-asap
-- |-appointment
-- |+social_entity
--  |-circle
--  |-contact
-- |-place

DROP VIEW "type";
CREATE VIEW "type" AS (
			SELECT information.id, 'note' as "type" FROM information, note WHERE information.id = note.id
	UNION	SELECT information.id, 'project' as "type" FROM information, project WHERE information.id = project.id
	UNION	SELECT information.id, 'asap' as "type"  FROM information, asap WHERE information.id = asap.id
	UNION	SELECT information.id, 'appointment' as "type" FROM information, appointment WHERE information.id = appointment.id
	UNION	SELECT information.id, 'circle' as "type" FROM information, circle WHERE information.id = circle.id
	UNION	SELECT information.id, 'contact' as "type" FROM information, contact WHERE information.id = contact.id
	UNION	SELECT information.id, 'place' as "type" FROM information, place WHERE information.id = place.id
	) ORDER BY id;
DROP VIEW "inbox";
CREATE VIEW "inbox" AS
	SELECT * FROM information WHERE inbox = TRUE;
DROP VIEW "later";
CREATE VIEW "later" AS
	SELECT * FROM information WHERE maybe = TRUE;
DROP VIEW "infoview" CASCADE;
CREATE VIEW "infoview" AS
	SELECT id, EXTRACT(EPOCH FROM created_at) AS created_at, EXTRACT(EPOCH FROM last_edited) AS last_edited FROM information;
CREATE VIEW asapview AS
	SELECT varchar 'asap' AS type, i.*, t.description, EXTRACT(EPOCH FROM t.completed) AS completed, l.name AS asaplist, a.project, p.description AS projectdescription FROM infoview i INNER JOIN task t USING (id) INNER JOIN asap a USING (id) LEFT OUTER JOIN task p ON a.project=p.id INNER JOIN asaplist l ON l.id = a.asaplist;
CREATE VIEW projectview AS
	SELECT varchar 'project' AS type, i.*, t.description, EXTRACT(EPOCH FROM t.completed) AS completed, p.parent FROM infoview i INNER JOIN task t USING (id) INNER JOIN project p USING (id);
CREATE VIEW "appointmentview" AS
	SELECT varchar 'appointment' AS type, i.*, "date", time, length, description FROM infoview i INNER JOIN appointment USING (id);
CREATE VIEW "noteview" AS
	SELECT varchar 'note' AS type, i.*, content, attachment, f.name AS attachmentname FROM infoview i JOIN note n USING (id) LEFT OUTER JOIN file f ON f.id = n.attachment;	
