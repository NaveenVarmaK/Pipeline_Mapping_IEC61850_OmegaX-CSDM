import requests
import json


class GraphDBConnector:
    def __init__(self, repository_url, repository_id):
        """
        Initialize GraphDB connector

        :param repository_url: Base URL of the GraphDB repository
        :param repository_id: ID of the specific repository
        """
        self.repository_url = repository_url.rstrip('/')
        self.repository_id = repository_id
        self.headers = {
            'Accept': 'application/sparql-results+json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def execute_query(self, query):
        """
        Execute a SPARQL query and return results

        :param query: SPARQL query string
        :return: Query results as a dictionary
        """
        # Construct the full endpoint URL
        endpoint = f"{self.repository_url}/repositories/{self.repository_id}"

        # Prepare the payload
        payload = f"query={requests.utils.quote(query)}"

        try:
            # Send POST request to GraphDB
            response = requests.post(
                endpoint,
                headers=self.headers,
                data=payload
            )

            # Raise an exception for bad responses
            response.raise_for_status()

            # Parse and return JSON results
            return response.json()

        except requests.RequestException as e:
            print(f"Error executing query: {e}")
            return None

    def print_query_results(self, results):
        """
        Pretty print query results

        :param results: Results dictionary from execute_query
        """
        if not results:
            print("No results to display.")
            return

        # Extract headers and rows
        headers = results.get('head', {}).get('vars', [])
        bindings = results.get('results', {}).get('bindings', [])

        # Print headers
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers))))

        # Print rows
        for row in bindings:
            row_values = []
            for header in headers:
                # Extract value, defaulting to 'N/A' if not found
                value = row.get(header, {}).get('value', 'N/A')
                row_values.append(str(value))
            print(" | ".join(row_values))


def main():
    # Example usage
    # Replace with your actual GraphDB repository details
    repository_url = "http://localhost:7200"  # Default GraphDB URL
    repository_id = "NarbonneKG"

    # Create connector
    graphdb = GraphDBConnector(repository_url, repository_id)

    # Example SPARQL query to get all device measurements
    example_query = """
    PREFIX prop: <https://w3id.org/omega-x/ontology/Property/>
    PREFIX ets: <https://w3id.org/omega-x/ontology/EventTimeSeries/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?dataPoint ?dataTime ?dataValue ?property ?unit
    WHERE {
        ?dataPoint rdf:type ets:DataPoint ;
               ets:dataTime ?dataTime ;
               ets:hasDataValue ?dataValue ;
               prop:isAboutProperty ?property ;
               prop:hasUnit ?unit .
    }
    """

    # Execute query
    results = graphdb.execute_query(example_query)

    # Print results
    if results:
        graphdb.print_query_results(results)


if __name__ == "__main__":
    main()