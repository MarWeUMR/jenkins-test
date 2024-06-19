import jaydebeapi
import glob
import os
import pandas as pd

def impala():
    # Creates a list of jar files in the /path/to/jar/files/ directory
    jar_files_impala = glob.glob('/home/jenkins/libs/*.jar')
    print(jar_files_impala)

    host='10.11.4.1'
    port='8443'
    database='default'
    user = os.getenv('IMPALA_USER')
    password = os.getenv('IMPALA_PASSWORD')

    print(user)
    print(password)

    driver_impala='com.cloudera.impala.jdbc.Driver'

    conn_str_impala = (
        f"jdbc:impala://{host}:{port}/{database};"
        f"ssl=1;transportMode=http;httpPath=gateway/cdp-proxy-api/impala;"
        f"AuthMech=3;UID={user};PWD={password};"
        f"AllowSelfSignedCerts=1;AllowHostNameCNMismatch=1"
    )

    print(conn_str_impala)

    try:
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

        # Write DataFrame to CSV
        csv_file_path = 'output/results.csv'
        df.to_csv(csv_file_path, index=False)
        print(f"Data written to {csv_file_path}")

        # Close the cursor and connection
        cursor.close()
        conn_impala.close()
    except Exception as e:
        print(f"Error: {e}")

def main():
    impala()

if __name__ == "__main__":
    main()

