import jaydebeapi
import glob
import os
import pandas as pd

def impala():
    # Creates a list of jar files in the /path/to/jar/files/ directory
    jar_files_impala = glob.glob('/root/libs/*.jar')
    print(jar_files_impala)

    host='cloudera-dev-heavy.cloudera.sva.dev'
    port='8443'
    database='default'
    user = os.getenv('IMPALA_USER')
    password = os.getenv('IMPALA_PASSWORD')

    driver_impala='com.cloudera.impala.jdbc.Driver'

    conn_str_impala = (
        f"jdbc:impala://{host}:{port}/{database};"
        f"ssl=1;transportMode=http;httpPath=gateway/cdp-proxy-api/impala;"
        f"AuthMech=3;UID={user};PWD={password};"
        f"AllowSelfSignedCerts=1;AllowHostNameCNMismatch=1"
    )

    print(conn_str_impala)

    conn_impala = jaydebeapi.connect(
        driver_impala,
        conn_str_impala,
        jars=jar_files_impala,
    )

    # Create a cursor and execute a query
    cursor = conn_impala.cursor()
    cursor.execute('SELECT * FROM sample_data')

    # Fetch the results
    results = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    # Create a DataFrame for better visualization
    df = pd.DataFrame(results, columns=columns)
    print(df)

    # Close the cursor and connection
    cursor.close()
    conn_impala.close()

def main():
    impala()

if __name__ == "__main__":
    main()

