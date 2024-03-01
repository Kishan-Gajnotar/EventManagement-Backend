FETCH_EVENT_DETAILS = '''
                        select *
                        from events
                    '''

CREATE_NEW_EVENT = '''
                    INSERT INTO events (event_name, start_time, end_time, location, description, category, banner_image_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                '''

FETCH_EVENT_BY_ID = '''
                    SELECT *
                    FROM events
                    WHERE event_id = %s
                    '''

DELETE_EVENT_BY_ID = '''
                     DELETE FROM events
                     WHERE event_id = %s
                     '''

UPDATE_EVENT = '''
                UPDATE events
                SET event_name = %s, start_time = %s, end_time = %s,
                    location = %s, description = %s, category = %s, banner_image_url = %s
                WHERE event_id = %s
              '''

CHECK_EVENT_BY_NAME = '''
                        SELECT *
                        FROM events
                        WHERE event_name = %s
                    '''

