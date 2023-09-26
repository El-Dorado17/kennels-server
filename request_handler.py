#CHAPTER 1
#the request comes here first and we check top see which module it needs to go to.
#(see animal requests)

#GET, POST, DELETE, AND PUT are all here
#doOptions handles OPTIONS request and allows the appropiate CORS Headers to communicate across domains
#If we could communicate across any domain ever, the application wouldn't be very secure

# add this import to the top of the file
from urllib.parse import urlparse, parse_qs
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views.animal_requests import create_animal, delete_animal
from views.location_requests import create_location, delete_location
from views.employee_requests import create_employee, delete_employee
from views.customer_requests import create_customer, delete_customer
from views.animal_requests import update_animal
from views.customer_requests import update_customer
from views.employee_requests import update_employee
from views.location_requests import update_location
from views.animal_requests import get_all_animals, get_single_animal
from views.customer_requests import get_all_customers, get_single_customer
from views.employee_requests import get_all_employees, get_single_employee
from views.location_requests import get_all_locations, get_single_location
from views.customer_requests import get_customers_by_email
from views.animal_requests import get_animals_by_location
from views.animal_requests import get_animals_by_status
from views.employee_requests import get_employees_by_location

#? Here's a class. It inherits from another class.
#? For now, think of a class as a container for functions that work together for a common purpose.
#? In this case, that common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
#? This is a Docstring it should be at the beginning of all classes and functions
#? It gives a description of the class or function:
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""
#? Here's a class function Here's a method on the class that overrides the parent's method.
#? It handles any GET request.
    def do_GET(self):
        """retreives whatever resource we ask for"""

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
            elif resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()
            elif resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                response = get_customers_by_email(query['email'][0])
            elif query.get('location_id') and resource == 'animals':
                response = get_animals_by_location(query['location_id'][0])
            elif query.get('status') and resource == 'animals':
                response = get_animals_by_status(query['status'][0])
            elif query.get('location_id') and resource == 'employees':
                response = get_employees_by_location(query['location_id'][0])

        if response is not None:
            self._set_headers(200)
        else:
            self._set_headers(404)

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """POST REQUESTS | POST REQUESTS"""
        # self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_location = None
        new_employee = None
        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                created_resource = create_location(post_body)
            else:
                self._set_headers(400)
                created_resource = {
                "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_animal).encode())

        if resource == "locations":
            new_location = create_location(post_body)
            self.wfile.write(json.dumps(new_location).encode())
        if resource == "employees":
            new_employee = create_employee(post_body)
            self.wfile.write(json.dumps(new_employee).encode())
        if resource == "customers":
            new_customer = create_customer(post_body)
            self.wfile.write(json.dumps(new_customer).encode())

    def do_DELETE(self):
        """THE DELETE"""
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        if resource == "locations":
            delete_location(id)
        if resource == "customers":
            delete_customer(id)
        if resource == "employees":
            delete_employee(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handles all the put requests"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False
        
        # Delete a single animal from the list
        if resource == "animals":
            success = update_animal(id, post_body)
        if resource == "locations":
            success = update_location(id, post_body)
        if resource == "customers":
            success = update_customer(id, post_body)
        if resource == "employees":
            success = update_employee(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response
        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
            'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
            'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
