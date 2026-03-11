# Prosegur Smart API Documentation

The below documentation provides details on how to interact with the Prosegur Smart API. There is no public documentation for the API so the below has been extracted by intercepting network traffic from the official Prosegur Smart mobile application. Put another way, this is unofficial documentation to help during the development process. The samples that have been included have been anonymized to remove any sensitive information so values may differ from actual API responses.

Base URL: `https://api-smart.prosegur.cloud/smart-server/ws`

## Table of Contents

- [Authentication](#authentication)
- [Installations](#installations)
- [Panel Status](#panel-status)
- [Control Alarm Status](#control-alarm-status)
- [Installation Details](#installation-details)
- [Supported Countries](#supported-countries)
- [Common Headers](#common-headers)
- [Response Structure](#response-structure)

## Common Headers

All requests require the following headers:

```http
User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Origin: https://alarmas.movistarproseguralarmas.es
Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html
```

For authenticated requests, additionally include:

```http
X-Smart-Token: <token-from-login-response>
```

## Response Structure

All API responses follow this structure:

```json
{
  "result": {
    "code": 200,
    "message": "descriptive message",
    "description": "OK"
  },
  "data": { ... }
}
```

## Authentication

### Login

Authenticate a user and obtain an access token.

**Endpoint:** `POST /access/login`

**Request Body:**

```json
{
  "user": "username",
  "password": "password",
  "language": "en_GB",
  "origin": "ES",
  "platform": "smart2",
  "provider": "none"
}
```

**Parameters:**

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| user      | string | Yes      | Username (email)                     |
| password  | string | Yes      | User password                        |
| language  | string | Yes      | Language code (e.g., "en_GB")        |
| origin    | string | Yes      | Country code (see [Supported Countries](#supported-countries)) |
| platform  | string | Yes      | Platform identifier (e.g., "smart2") |
| provider  | string | Yes      | Provider identifier (e.g., "none")   |

**Success Response (200):**

**Sample Response:** [api-samples/login_success.json](api-samples/login_success.json)

**Key Response Fields:**

| Field         | Type   | Description                                      |
|---------------|--------|--------------------------------------------------|
| token         | string | JWT access token (use in X-Smart-Token header)   |
| refresh_token | string | JWT refresh token for obtaining new access token |
| username      | string | User's email address                             |
| name          | string | User's first name                                |
| surnames      | string | User's last name(s)                              |
| clientId      | string | Unique client identifier                         |
| administrator | int    | Administrator flag (1 = admin, 0 = regular user) |
| services      | object | Available services for the user                  |

**cURL Example:**

```bash
curl -X POST \
  -H "User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0" \
  -H "Accept: application/json, text/plain, */*" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "Origin: https://alarmas.movistarproseguralarmas.es" \
  -H "Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html" \
  "https://api-smart.prosegur.cloud/smart-server/ws/access/login" \
  -d '{
    "user": "username",
    "password": "password",
    "language": "en_GB",
    "origin": "ES",
    "platform": "smart2",
    "provider": "none"
  }'
```

---

## Installations

### List Installations

Retrieve all installations associated with the authenticated user.

**Endpoint:** `GET /installation`

**Authentication:** Required (X-Smart-Token header)

**Success Response (200):**

**Sample Response:** [api-samples/installation.json](api-samples/installation.json)

**Key Response Fields:**

| Field            | Type    | Description                                 |
|------------------|---------|---------------------------------------------|
| installationId   | string  | Unique installation identifier              |
| description      | string  | Installation description/address            |
| installationType | string  | Type of installation (e.g., "CLIMAX")       |
| status           | string  | Current status (e.g., "DA" = Disarmed)      |
| pinControl       | boolean | Whether PIN control is enabled              |
| hasDomotic       | boolean | Whether domotic features are available      |
| detectors        | array   | List of detectors (cameras, sensors, etc.)  |
| partitions       | array   | List of partitions/zones                    |
| services         | array   | Available services with status codes        |
| latitude         | string  | GPS latitude coordinate                     |
| longitude        | string  | GPS longitude coordinate                    |
| contractActive   | boolean | Whether the contract is active              |
| contractNumber   | string  | Contract number                             |

**Detector Object:**

| Field       | Type    | Description                           |
|-------------|---------|---------------------------------------|
| id          | string  | Unique detector identifier            |
| description | string  | Detector description/location         |
| type        | string  | Detector type (e.g., "Camera")        |
| streaming   | boolean | Whether streaming is enabled          |

**Partition Object:**

| Field          | Type   | Description                     |
|----------------|--------|---------------------------------|
| id             | number | Unique partition identifier     |
| installationId | number | Associated installation ID      |
| key            | number | Partition key/number            |
| name           | string | Partition name                  |
| status         | string | Partition status (e.g., "DA")   |


**cURL Example:**

```bash
curl -H "User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0" \
  -H "Accept: application/json, text/plain, */*" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "Origin: https://alarmas.movistarproseguralarmas.es" \
  -H "X-Smart-Token: <token-from-login>" \
  -H "Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html" \
  "https://api-smart.prosegur.cloud/smart-server/ws/installation"
```

---

## Installation Details

### Get Installation by ID

Retrieve detailed information about a specific installation.

**Endpoint:** `GET /installation/{installationId}`

**Authentication:** Required (X-Smart-Token header)

**Path Parameters:**

| Parameter      | Type   | Required | Description                     |
|----------------|--------|----------|---------------------------------|
| installationId | string | Yes      | Unique installation identifier  |

**Success Response (200):**

**Sample Response:** [api-samples/installation-number.json](api-samples/installation-number.json)

**cURL Example:**

```bash
curl -H "User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0" \
  -H "Accept: application/json, text/plain, */*" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "Origin: https://alarmas.movistarproseguralarmas.es" \
  -H "X-Smart-Token: <token-from-login>" \
  -H "Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html" \
  "https://api-smart.prosegur.cloud/smart-server/ws/installation/16354"
```

---

## Panel Status

### Get Panel Status

Retrieve the current status of an installation's alarm panel.

**Endpoint:** `GET /installation/{installationId}/panel-status`

**Authentication:** Required (X-Smart-Token header)

**Path Parameters:**

| Parameter      | Type   | Required | Description                     |
|----------------|--------|----------|---------------------------------|
| installationId | string | Yes      | Unique installation identifier  |

**Success Response (200):**

**Sample Response:** [api-samples/panel-status.json](api-samples/panel-status.json)

**Key Response Fields:**

| Field      | Type   | Description                                |
|------------|--------|--------------------------------------------|
| status     | string | Overall panel status (e.g., "DA")          |
| partitions | array  | List of partitions with individual status |



| AT        | Armed (Total)                              |
| DA        | Disarmed                                   |
| error     | Error                                      |
| AP        | Armed Partially                            |
| FC        | Power Failure                              |
| RFC       | Power Restored                             |
| IM        | Image                                      |
| EDA       | Error - Disarmed                           |
| EAT       | Error - Armed Total                        |
| EAP       | Error - Armed Partially                    |
| EAT-COM   | Error - Armed Total (Communications)       |
| EDA-COM   | Error - Disarmed (Communications)          |
| EAP-COM   | Error - Armed Partially (Communications)   |
| EIM-COM   | Error - Image (Communications)             |

**cURL Example:**

```bash
curl -H "User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0" \
  -H "Accept: application/json, text/plain, */*" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "Origin: https://alarmas.movistarproseguralarmas.es" \
  -H "X-Smart-Token: <token-from-login>" \
  -H "Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html" \
  "https://api-smart.prosegur.cloud/smart-server/ws/installation/16354/panel-status"
```

---

## Control Alarm Status

Change the alarm status (arm or disarm) for an installation or specific partitions within an installation.

**Endpoint:** `PUT /installation/{installationId}/status`

**Authentication:** Required (X-Smart-Token header)

**Path Parameters:**

| Parameter      | Type   | Required | Description                     |
|----------------|--------|----------|---------------------------------|
| installationId | string | Yes      | Unique installation identifier  |

**Request Body:**

```json
{
  "statusCode": "AP"
}
```

**Request Parameters:**

| Parameter  | Type   | Required | Description                                                      |
|------------|--------|----------|------------------------------------------------------------------|
| statusCode | string | Yes      | Desired status code (DA, AP, or AT)                              |
| partitions | array  | No       | Array of partition keys to control. If omitted, affects all partitions |

**Status Code Values:**

| Code | Description     | Action                                    |
|------|-----------------|-------------------------------------------|
| DA   | Disarmed        | Disarms the alarm                         |
| AP   | Armed Partially | Arms the alarm in partial/night mode      |
| AT   | Armed Total     | Fully arms the alarm (away mode)          |

**Example 1: Arm Partially (All Partitions)**

```json
{
  "statusCode": "AP"
}
```

**Example 2: Disarm (All Partitions)**

```json
{
  "statusCode": "DA"
}
```

**Example 3: Disarm Specific Partition**

```json
{
  "statusCode": "DA",
  "partitions": [
    "2"
  ]
}
```

**Success Response (200):**

```json
{
  "result": {
    "code": 200,
    "description": "OK",
    "message": "Status updated successfully"
  },
  "data": null
}
```

**cURL Example - Arm Partially:**

```bash
curl -X PUT \
  -H "User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0" \
  -H "Accept: application/json, text/plain, */*" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "Origin: https://alarmas.movistarproseguralarmas.es" \
  -H "X-Smart-Token: <token-from-login>" \
  -H "Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html" \
  "https://api-smart.prosegur.cloud/smart-server/ws/installation/16354/status" \
  -d '{"statusCode": "AP"}'
```

**cURL Example - Disarm:**

```bash
curl -X PUT \
  -H "User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0" \
  -H "Accept: application/json, text/plain, */*" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "Origin: https://alarmas.movistarproseguralarmas.es" \
  -H "X-Smart-Token: <token-from-login>" \
  -H "Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html" \
  "https://api-smart.prosegur.cloud/smart-server/ws/installation/16354/status" \
  -d '{"statusCode": "DA"}'
```

**cURL Example - Disarm Specific Partition:**

```bash
curl -X PUT \
  -H "User-Agent: Smart/1 CFNetwork/3826.400.120 Darwin/24.3.0" \
  -H "Accept: application/json, text/plain, */*" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "Origin: https://alarmas.movistarproseguralarmas.es" \
  -H "X-Smart-Token: <token-from-login>" \
  -H "Referer: https://alarmas.movistarproseguralarmas.es/smart-mv/login.html" \
  "https://api-smart.prosegur.cloud/smart-server/ws/installation/16354/status" \
  -d '{"statusCode": "DA", "partitions": ["2"]}'
```

**Notes:**

- Partition keys are strings representing the partition number ("1", "2", etc.)
- If the `partitions` array is omitted, the status change applies to all partitions in the installation
- Use the [Get Panel Status](#get-panel-status) endpoint to verify the status change was successful
- Status changes may take a few seconds to be reflected in the panel

---

## Supported Countries

The API supports the following countries with their specific configurations:

| Country Code | Country    | Origin URL                                        | Referer URL                                                            | Origin Type |
|--------------|------------|---------------------------------------------------|------------------------------------------------------------------------|-------------|
| AR           | Argentina  | https://smart.prosegur.com/smart-individuo        | https://smart.prosegur.com/smart-individuo/login.html                  | Web         |
| PY           | Paraguay   | https://smart.prosegur.com/smart-individuo        | https://smart.prosegur.com/smart-individuo/login.html                  | Web         |
| PT           | Portugal   | https://smart.prosegur.com/smart-individuo        | https://smart.prosegur.com/smart-individuo/login.html                  | Web         |
| ES           | Spain      | https://alarmas.movistarproseguralarmas.es        | https://alarmas.movistarproseguralarmas.es/smart-mv/login.html         | WebM        |
| CO           | Colombia   | https://smart.prosegur.com/smart-individuo        | https://smart.prosegur.com/smart-individuo/login.html                  | Web         |
| UY           | Uruguay    | https://smart.prosegur.com/smart-individuo        | https://smart.prosegur.com/smart-individuo/login.html                  | Web         |

**Note:** When making requests for different countries, ensure you use the correct `Origin` and `Referer` headers corresponding to the country code. The examples in this documentation use Spain (ES) configuration.

---

## Notes

- The `X-Smart-Token` header must be included in all authenticated requests
- Tokens expire after a certain period; use the `refresh_token` to obtain a new access token
- The API uses HTTPS for all communications
