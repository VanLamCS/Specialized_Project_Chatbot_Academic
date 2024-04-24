# Server chatbot

## Python

### python v3.10.4

## Run server

### Step 1

Switch location at `server`

### Step 2

Create virtual environment
`python -m venv venv`

Activate:

On Windows
`./venv/Scripts/activate`

On Linux
`source venv/bin/activate`

### Step 3

Install packages in requirements.txt
`pip install -r requirements.txt`

### Step 4

Edit environment variables in `.env`

### Step 5

Run server
`python app.py`

## APIs

### Login

`POST api/user/login`

Header: Null

Body

```json
{
  "email": "template@email.com",
  "password": "123456"
}
```

### Register

`POST api/user/register`

Header: Null
Body:

```json
{
  "name": "Le Van Lam",
  "email": "vanlam@gmail.com",
  "password": "123456"
}
```

### Create conversation

`POST api/conversation/create`

Header:

```json
{
  "Authorization": "Bearer <access_token>"
}
```

Body:

```json
{
  "name": "Chat 01" //(optional. Default: Default chat)
}
```

### Retrive own conversation

`GET api/conversation/get-mine`
Header:

```json
{
  "Authorization": "Bearer <access_token>"
}
```

### Edit conversation name

`POST api/conversation/change-name`
Header:

```json
{
  "Authorization": "Bearer <access_token>"
}
```

Body:

```json
{
  "name": "Chat 01",
  "conversation_id": "id of conversation"
}
```

### Retrieve conversation history

`GET api/conversation/history`

Header:

```json
{
  "Authorization": "Bearer <access_token>"
}
```

Params:

```json
{
  "conversation_id": "id",
  "page": 1, // (optional. Default: 1)
  "limit": 50 // (optional. Default: 50)
}
```

### Delete conversation

`DELETE api/conversation`

Header:

```json
{
  "Authorization": "Bearer <access_token>"
}
```

Body:

```json
{
  "conversation_id": "id"
}
```

### Send message

`POST api/message/send`

Header:

```json
{
  "Authorization": "Bearer <access_token>"
}
```

Body:

```json
{
  "message": "Halo",
  "conversation_id": "id of conversation"
}
```
