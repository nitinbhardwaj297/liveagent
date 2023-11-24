import os

from langchain.llms import OpenAI

# from translate import eng_to_yo, yo_to_eng

from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chains.question_answering import load_qa_chain

from langchain.vectorstores import Chroma

import openai

# from vectorize import create_db

os.environ["OPENAI_API_KEY"] = "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"

persist_directory_faq = "actions/demo_db_faq"
persist_directory_slang = "actions/demo_db_slang"

llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

embeddings = OpenAIEmbeddings()

chain = load_qa_chain(llm=llm, verbose=True, chain_type="stuff")

vector_db_faq = Chroma(
    persist_directory=persist_directory_faq, embedding_function=embeddings
)
vector_db_slang = Chroma(
    persist_directory=persist_directory_slang, embedding_function=embeddings
)


def chat_with_memory(full_prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant and you are expert in content writing.",
            },
            {"role": "user", "content": full_prompt},
        ],
    )

    return completion.choices[0].message


def get_answer(query: str):
    # save_data(query)
    # print("Data is collected and saved")

    # create_db()
    # print("Vector Database Created")

    ##persist_directory_faq = "demo_db_faq"
    ##persist_directory_slang = "demo_db_slang"

    ##llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

    ##embeddings = OpenAIEmbeddings()

    ##chain = load_qa_chain(llm=llm, verbose=True, chain_type="stuff")

    ##vector_db = Chroma(
    ##    persist_directory=persist_directory, embedding_function=embeddings
    ##)
    ##en_query = yo_to_eng(query)
    ##mathcing_docs = vector_db.similarity_search(en_query)  # cosine euclidean mmr

    ##answer = chain.run(input_documents=mathcing_docs, question=en_query)  # top_k
    # Please answer the question from the context, just say i don't know
    ##yo_ans = eng_to_yo(answer)

    # above code is for translation

    ##en_query = yo_to_eng(query)
    mathcing_docs_faq = vector_db_faq.similarity_search(query)
    mathcing_docs_slang = vector_db_slang.similarity_search(query)
    print(mathcing_docs_faq)
    print(mathcing_docs_slang)
    final_str = f"""
        Answer the query based on the FAQ context provided. If you do not understand the query, refer to the Slang Context, but use it only for understanding the query, not for showing the meaning of slang words. Show only the response based on the query and do not mention FAQ or slang in your response.

        FAQ Context: {mathcing_docs_faq}
        Slang Context: {mathcing_docs_slang}
        Query: {query}
        """

    print("fianl", final_str)

    answer = chat_with_memory(final_str)  # cosine euclidean mmr
    return str(answer["content"])
    # answer = chain.run(input_documents=mathcing_docs, question=query)  # top_k
    # Please answer the question from the context, just say i don't know
    ##yo_ans = eng_to_yo(answer)
    # return answer


# query = "iru awọn ọna idena oyun wo lo wa? "
# print(get_answer(query))
