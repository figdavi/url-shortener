https://roadmap.sh/projects/url-shortening-service

## TODO

- [x] return a 201 Created status code with the newly created short URL or a 400 Bad Request status code with error messages in case of validation errors. Short codes must be unique and should be generated randomly.
- [x] use the following format for time: "2021-09-01T12:00:00Z"
- [x] create utils.py
- [x] add update endpoint 
- [x] add delete endpoint
- [x] add stats endpoint
- [ ] add response models
- [ ] pydantic models for db
- [ ] review url validation
- [ ] https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure
- [ ] ORM