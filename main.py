import jaydebeapi
import glob
import os
import structlog
import pandas as pd

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer(colors=True),
    ]
)
log = structlog.get_logger()

def impala():
    # Creates a list of jar files in the /home/jenkins/libs/ directory
    jar_files_impala = glob.glob('/home/jenkins/libs/*.jar')
    log.info("Jar files loaded", jar_files=jar_files_impala)

    host='10.11.4.1'
    port='8443'
    database='default'
    user = os.getenv('IMPALA_USER')
    password = os.getenv('IMPALA_PASSWORD')

    log.info("Database credentials", user=user, password=password)

    driver_impala='com.cloudera.impala.jdbc.Driver'

    conn_str_impala = (
        f"jdbc:impala://{host}:{port}/{database};"
        f"ssl=1;transportMode=http;httpPath=gateway/cdp-proxy-api/impala;"
        f"AuthMech=3;UID={user};PWD={password};"
        f"AllowSelfSignedCerts=1;AllowHostNameCNMismatch=1"
    )

    log.info("Connection string", connection_string=conn_str_impala)

    try:
        conn_impala = jaydebeapi.connect(
            driver_impala,
            conn_str_impala,
            jars=jar_files_impala,
        )

        # Create a cursor and execute a query
        cursor = conn_impala.cursor()
        cursor.execute('SELECT * FROM sample_dat')

        # Fetch the results
        results = cursor.fetchall()

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Create a DataFrame for better visualization
        df = pd.DataFrame(results, columns=columns)
        log.debug("Query results", dataframe_info=df.head().to_dict())

        # Define the output directory and file
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        csv_file_path = os.path.join(output_dir, 'results.csv')

        # Write DataFrame to CSV
        df.to_csv(csv_file_path, index=False)
        log.info("Data written to CSV", file_path=csv_file_path)

        # Close the cursor and connection
        cursor.close()
        conn_impala.close()
    except Exception as e:
        log.error("Error occurred", exception=str(e))
        log.exception("Exception occurred", exception=str(e))

def main():
    impala()

if __name__ == "__main__":
    main()
