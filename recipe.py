import tkinter as tk
from tkinter import messagebox, scrolledtext
from googletrans import Translator
import requests


class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Finder")

        self.root.geometry("500x400")
        self.root.eval('tk::PlaceWindow . center')

        self.entry_label = tk.Label(root, text="Enter a meal:")
        self.entry_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.meal_entry = tk.Entry(root)
        self.meal_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.search_button = tk.Button(root, text="Search", command=self.search_recipe)
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.recipe_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=60)
        self.recipe_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def search_recipe(self):
        meal_name = self.meal_entry.get().strip()
        if not meal_name:
            messagebox.showwarning("Warning", "Please enter a meal name.")
            return

        translator = Translator()
        translated_result = translator.translate(meal_name, src='auto', dest='en')
        translated_meal_name = translated_result.text

        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={translated_meal_name}"
        response = requests.get(url)
        data = response.json()

        if "meals" not in data:
            self.recipe_text.delete("1.0", tk.END)
            self.recipe_text.insert(tk.END, "Recipe not found.")
        else:
            self.display_recipes(data["meals"])

    def display_recipes(self, meals):
        self.recipe_text.delete("1.0", tk.END)
        if len(meals) == 1:
            self.display_recipe(meals[0])
        else:
            self.recipe_text.insert(tk.END, "Select a recipe:\n")
            for idx, meal in enumerate(meals, start=1):
                self.recipe_text.insert(tk.END, f"{idx}. {meal['strMeal']}\n")

            self.recipe_text.bind("<Button-1>", lambda event: self.on_recipe_click(event, meals))

    def on_recipe_click(self, event, meals):
        index = self.recipe_text.index(tk.CURRENT).split(".")[0]
        selected_meal = meals[int(index) - 1]
        self.display_recipe(selected_meal)

    def display_recipe(self, meal):
        self.recipe_text.delete("1.0", tk.END)
        self.recipe_text.insert(tk.END, f"Meal: {meal['strMeal']}\n\n")
        self.recipe_text.insert(tk.END, f"Category: {meal['strCategory']}\n\n")
        self.recipe_text.insert(tk.END, "Ingredients:\n")

        for i in range(1, 21):
            ingredient_key = f"strIngredient{i}"
            measure_key = f"strMeasure{i}"
            ingredient = meal.get(ingredient_key)
            measure = meal.get(measure_key)
            if ingredient:
                self.recipe_text.insert(tk.END, f"- {measure} {ingredient}\n")

        self.recipe_text.insert(tk.END, "\nInstructions:\n")
        self.recipe_text.insert(tk.END, meal["strInstructions"])


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
