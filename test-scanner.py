import unittest
from unittest.mock import patch, MagicMock
import scanner

class TestScanner(unittest.TestCase):
    @patch("scanner.socket.socket")
    def test_scan_port_open(self, mock_socket):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_socket.return_value.__enter__.return_value = mock_sock

        result = scanner.scan_port("127.0.0.1", 80)
        self.assertEqual(result[0], 80)

    @patch("scanner.socket.socket")
    def test_scan_port_closed(self, mock_socket):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 1
        mock_socket.return_value.__enter__.return_value = mock_sock

        result = scanner.scan_port("127.0.0.1", 81)
        self.assertIsNone(result)

    @patch("scanner.scan_port")
    def test_scan_ports(self, mock_scan_port):
        mock_scan_port.side_effect = [(22, "ssh"), None, (80, "http")]
        result = scanner.scan_ports("127.0.0.1", [22, 23, 80], workers=3)
        self.assertEqual(result, [(22, "ssh"), (80, "http")])

if __name__ == "__main__":
    unittest.main()