# NASA API Backend Services

---
### API Documentation

<br>

Service URL: 
https://l1zxnfptyk.execute-api.ap-southeast-1.amazonaws.com/dev/

<br>

1. Get Solar Angle
    ```
    GET /angle
    ```

    Request Parameter(s):
    ```
    ?latitude=123&longitude=123
    ```

2. Get Solar Irradiance
    ```
    GET /irradiance
    ```

    Request Parameter(s):
    ```
    ?latitude=123&longitude=123&start=2019&end=2020
    ```

3. Get Sky Details (Cloud too)
    ```
    GET /sky
    ```

    Request Parameter(s):
    ```
    ?latitude=123&longitude=123&mode=daily&start=2019&end=2020
    ```

4. Get Average (Calculated)
    ```
    GET /average
    ```

    Request Parameter(s):
    ```
    ?latitude=123&longitude=123&start=2019&end=2020
    ```
