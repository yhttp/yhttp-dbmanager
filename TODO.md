Readme
 - badges

Github CI/CD
PyPi


```python
    self.create_objects(args)
    self.report_objects(args)

def create_objects(self, args):
    app = args.application
    orm.initialize(app.db, app.settings.db.url, create_objects=True)

def report_objects(self, args):
    app = args.application
    result = app.db.execute('''
        SELECT relname, relkind
        FROM pg_class
        WHERE relname !~ '^(pg|sql)_' AND relkind != 'v';
    ''')
    print('Following objects has been created successfully:')
    for name, kind in result.fetchall():
        print(kind, name)
```
