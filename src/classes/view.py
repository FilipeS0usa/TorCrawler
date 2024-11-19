
class View:

    def show_error(self, e):
        """

        Shows the error message
        :param e:
        :return:
        """
        print(f"An error ocurred: {e}")
        print(f"Error type: {type(e).__name__}")

    def show_message(self, message):
        """

        Show a message
        :param message:
        :return:
        """
        print(message)

