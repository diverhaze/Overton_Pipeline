from germansentiment import SentimentModel
#import csvhandler
#import datarefiner
#import documenter
import logging

# Initialisation
doc = documenter.Documenter()       # Logging
model = SentimentModel()            # Actual ML-Model by Oliver Guhr
dr = datarefiner.DataRefiner()      # data refining
csv = csvhandler.CsvHandler(dr)     # csv reader/writer; CSV_Handler must get a DataRefiner Object

string_source = "taz_filtered_christian_kahmann.csv"
string_results = "results_1.csv"
string_test = "test_2.csv"

logging.info("Model and classes loaded")


def write_data(information_list, filename):
    for text in information_list:
        article_id = text.pop(0)                # get article ID
        date = text.pop(0)                     # get article date
        result = model.predict_sentiment(text)  # call BERT

        tensors_title, tensors_text = dr.clear_logits(result[0].logits)   # get tensor values
        print(f"Id: {article_id} /// Title: {tensors_title} /// Text: {tensors_text}", end=': ')

        csv.write_result_csv(filename, article_id, date, tensors_title, tensors_text)  # write output csv
        # CSV schreiber muss wahrscheinlich noch von Liste in String geparsed werden


if __name__ == '__main__':

    data = csv.load_csv(string_source, 0)                   # load CSV and convert into list
    csv.create_result_csv(string_test)                  # create output CSV
    write_data(data, string_test)                                     # Run BERT and write output CSV

    results = csv.load_csv(string_test, 1)               # load result CSV and convert into list
    print(dr.check_line_counts())                            # check if code ran smoothly so far
    #dr.find_amplitude(results)
