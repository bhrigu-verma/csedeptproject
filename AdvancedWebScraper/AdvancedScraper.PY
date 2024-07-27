#AdvancedScraper.PY
class DataType(Enum):
                cleaned_result = self.clean_text(result) if clean else result
                print(f"{cleaned_result}\n")
        else:
            print("No data found based on the specified criteria.")

    def save_results(self, output_format):
        if output_format == OutputFormat.TEXT_FILE.value:
            self.save_results_to_text_file()
        elif output_format == OutputFormat.JSON.value:
            self.save_results_to_json()
        elif output_format == OutputFormat.CSV.value:
            self.save_results_to_csv()
        elif output_format == OutputFormat.PRINT.value:
            pass  # Results are already printed

    def save_results_to_text_file(self):
        with open('output.txt', 'w', encoding='utf-8') as file:
            for result in self.results:
                file.write(result + '\n')
        print("Data saved to output.txt")

    def save_results_to_json(self):
        with open('output.json', 'w', encoding='utf-8') as file:
            json.dump(self.results, file, indent=2)
        print("Data saved to output.json")

    def save_results_to_csv(self):
        with open('output.csv', 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Result'])
            for result in self.results:
                csv_writer.writerow([result])
        print("Data saved to output.csv")

async def main():
    scraper = AdvancedWebScraper()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        url = input("Please enter the URL: ")

        while True:
            try:
                data_type = int(input(f"Please enter data type {', '.join([f'({dt.value}: {dt.name})' for dt in DataType])}: "))
                if data_type in DataType._value2member_map_:
                    break
                else:
                    print("Invalid data type. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        query = input("Enter the query: ") if data_type == DataType.SEARCH_QUERY.value else None
        custom_tag = input("Enter Custom Tag: ") if data_type == DataType.CUSTOM_TAG.value else None

        try:
            await scraper.extract_data(page, url, data_type, query, custom_tag)
            scraper.display_results(clean=True)

            # Offer user choice to print, save as a text file, JSON, or CSV
            output_format = int(input("Save output as (1: text file, 2: json, 3: csv): "))
            if 0 <= output_format <= 3:
                scraper.save_results(output_format)

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
