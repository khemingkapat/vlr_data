from dash import Dash,html
from src.components.layout import create_layout
def main() -> None:
    print("Hello World")
    app = Dash() 
    app.title = 'Medal dashboard'
    app.layout = create_layout(app)
    app.run()

if __name__ == "__main__":
    main()
