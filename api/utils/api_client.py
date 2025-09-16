import requests
from requests.exceptions import HTTPError, JSONDecodeError, RequestException
from requests.adapters import HTTPAdapter, Retry

class APIClient:
    def __init__(self, base_url, token=None, max_retries=5):
        self.base_url = base_url
        self.session = requests.Session()

        # Configurar reintentos
        retries = Retry(
            total=max_retries,
            backoff_factor=1,  # espera exponencial: 1s, 2s, 4s...
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.headers = {}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, headers=self.headers, params=params)

    def post(self, endpoint, data):
        """Envía una petición POST con datos JSON."""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=data, headers=self.headers)

    def post_form(self, endpoint, data):
        """Envía una petición POST con datos en formato x-www-form-urlencoded."""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, data=data, headers=self.headers)

    def put(self, endpoint, json_data):
        """Envía una petición PUT con datos JSON."""
        url = f"{self.base_url}{endpoint}"
        return self.session.put(url, json=json_data, headers=self.headers)

    def delete(self, endpoint):
        """Envía una petición DELETE."""
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url, headers=self.headers)

    def patch(self, endpoint, json_data):
        """Envía una petición PATCH."""
        url = f"{self.base_url}{endpoint}"
        return self.session.patch(url, json=json_data, headers=self.headers)