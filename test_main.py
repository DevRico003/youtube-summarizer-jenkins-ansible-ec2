import sys
import unittest
from unittest.mock import patch, MagicMock
import main

class TestMainFunction(unittest.TestCase):

    @patch('main.st')
    @patch('main.get_transcript')
    @patch('main.summarize_with_langchain_and_openai')
    def test_main(self, mock_summarize, mock_transcript, mock_st):
        # Mocken der Streamlit-Funktionen
        mock_st.text_input.return_value = 'https://www.youtube.com/watch?v=WaSn533G2IE'
        mock_st.button.return_value = True
        mock_st.progress.return_value = MagicMock()
        mock_st.empty.return_value = MagicMock()

        # Mocken der get_transcript und summarize_with_langchain_and_openai Funktionen
        mock_transcript.return_value = ("Transcript des Videos", "de")
        mock_summarize.return_value = "Zusammenfassung des Videos"

        # Aufrufen der main-Funktion
        main.main()

        # Überprüfen, ob die richtigen Funktionen aufgerufen wurden
        mock_transcript.assert_called_with('https://www.youtube.com/watch?v=WaSn533G2IE')
        mock_summarize.assert_called_with("Transcript des Videos", "de", 'gpt-3.5-turbo')

        # Absichtlich einen fehlerhaften Test hinzufügen
        self.assertEqual(1, 0, "Absichtlich fehlgeschlagener Test")

if __name__ == '__main__':
    test_suite = unittest.TestLoader().discover('.')
    test_result = unittest.TextTestRunner().run(test_suite)
    if test_result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
