# Restaurant Stats

## Description
A FastMCP server for accessing and updating the database created using JsonParser (jsonParser/README.md).
* Language
  * English
  * Programming
    * Python
* Type of Application
  * Server
  * fastmcp
* Author
  * Sam Swagger


## Future Plans
* Update fastmcp to v4

## Project Story
I originally had a lot of data that I wanted to build a database out of.
However, I didn't really want to write a long SQL statement to parse it into a database.
So instead, I built this app to interpret my data into a database schema based on the JSON object.
I then found out about fastmcp; so, I put 2 and 2 together, and created an MCP server for accessing the data from my database.

## How to run
First install [Docker](https://www.docker.com/products/docker-desktop/).
Then run the following command at the project root to build the container:
```bash
docker compose -f ./docker-compose.yml up
```
This will start the server at `localhost:8000`.
For more documentation on how to use fastmcp servers click [here](https://gofastmcp.com/getting-started/welcome)

## Note
This server is compatible with my [Chat Agent](https://github.com/sswagger/ChatAgent).
