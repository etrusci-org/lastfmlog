<?php
declare(strict_types=1);


/**
 * SQLite3 wrapper for the lazy.
 */
class DatabaseSQLite3 {
    protected $dbFile;
    protected $db;
    protected $encryptionKey;
    protected $sqliteVersion;

    /**
     * Class constructor.
     *
     * @param string $dbFile  Path to database file to use.
     * @param string $encryptionKey=''  Encryption key if any.
     * @return void
     */
    public function __construct(string $dbFile, string $encryptionKey='') {
        $this->dbFile = $dbFile;
        $this->encryptionKey = $encryptionKey;
        $this->sqliteVersion = SQLite3::version();
    }

    /**
     * Open the database.
     *
     * @param bool $rw=false  Whether to open the database with read+write instead of just read access.
     * @return bool  True on success.
     */
    public function open(bool $rw=false): bool {
        if ($this->db instanceof SQLite3) return false;

        $flag = (!$rw) ? SQLITE3_OPEN_READONLY : SQLITE3_OPEN_READWRITE;

        $this->db = new SQLite3($this->dbFile, $flag, $this->encryptionKey);

        if (!($this->db instanceof SQLite3)) return false;

        return true;
    }

    /**
     * Close the database.
     *
     * @return bool  True on success.
     */
    public function close(): bool {
        if (!($this->db instanceof SQLite3)) return false;

        $this->db->close();

        return true;
    }

    /**
     * Query the database.
     *
     * @param string $query  Query to execute.
     * @param array $values=array()  Query values.
     * @return array|bool  Query results or false on failure.
     */
    public function query(string $query, array $values=array()): array|bool {
        if (!($this->db instanceof SQLite3)) return false;

        $stmt = $this->db->prepare($query);
        if (!$stmt) return false;

        foreach ($values as $v) {
            $stmt->bindValue($v[0], $v[1], $v[2]);
        }

        $result = $stmt->execute();
        if (!$result) return false;

        $dump = array();
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $dump[] = $row;
        }

        $stmt->close();

        return $dump;
    }

    /**
     * Query the database for a single result.
     *
     * @param string $query  Query to execute.
     * @param array $values=array()  Query values.
     * @return array|bool  Query result.
     */
    public function querySingle(string $query, array $values=array()): array|bool {
        if (!($this->db instanceof SQLite3)) return false;

        $result = $this->query($query, $values);

        if (!$result || count($result) < 1) {
            return false;
        }

        return $result[0];
    }

    /**
     * Create, update or delete database data.
     *
     * @param string $query  Query to execute.
     * @param array $values=array()  Query values.
     * @return SQLite3Result|bool  SQLite3Result object or false on failure.
     */
    public function write(string $query, array $values=array()): SQLite3Result|bool {
        if (!($this->db instanceof SQLite3)) return false;

        $stmt = $this->db->prepare($query);

        if (!$stmt) return false;

        foreach ($values as $v) {
            $stmt->bindValue($v[0], $v[1], $v[2]);
        }

        return $stmt->execute();
    }
}
