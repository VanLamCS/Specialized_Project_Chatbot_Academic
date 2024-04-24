import torch
import torch.nn.functional as F

class Rag_helper:
    """
    A class to provide helper functions for document processing.
    """
    @staticmethod
    def extract_info_source(doc):
        """
        Extracts information from the source field of a document's metadata.

        Args:
            doc (object): The document to extract information from.

        Returns:
            tuple: A tuple containing two elements:
                - content (str): The content part of the source information.
                - effect_year (str): The effect year part of the source information.
        """

        return doc.metadata["source"].split(".")[0].split("/")[-1].split("_")[-2:]

    @staticmethod
    def add_info_docs(docs):
        """
        Adds content and effect_year fields to the metadata of each document in a list.

        Args:
            docs (list): A list of documents.

        Returns:
            list: The list of documents with updated metadata.
        """

        for doc in docs:
            infos = Rag_helper.extract_info_source(doc)
            doc.metadata["content"] = infos[0]
            doc.metadata["effect_year"] = infos[1]
        return docs

    @staticmethod
    def add_metadata_to_docs(docs):
      for doc in docs:
        doc.page_content = "(Nội dung được lấy từ tài liệu: \"" + doc.metadata["content"] + "\" và hiệu lực từ năm: " + doc.metadata["effect_year"] + ".)\n\n\n\n\""  + str(doc.page_content)  + "\""
      return docs

    @staticmethod
    def merge_docs(docs):
        """
        Merges documents with the same source, appending their page content.

        Args:
            docs (list): A list of documents.

        Returns:
            list: A list of merged documents with unique sources.
        """

        map_docs = []
        docs_merged = []

        for doc in docs:
            page_content, metadata = doc.page_content, doc.metadata

            if metadata["source"] in map_docs:
                index = map_docs.index(metadata["source"])
                docs_merged[index].page_content += "\n\n" + page_content
            else:
                docs_merged.append(doc)
                map_docs.append(metadata["source"])
        return docs_merged

    @staticmethod
    def confidence_score(scores, temperature=3.0):
        # Apply temperature scaling if needed
        if temperature != 1.0:
            scaled_scores = scores / temperature
        else:
            scaled_scores = scores

        # Apply softmax to get probabilities
        probabilities = F.softmax(scaled_scores, dim=-1)

        # Extract the maximum probability as the confidence score for each token
        confidence_scores = torch.max(probabilities, dim=-1).values

        # Calculate the average confidence score for the entire sequence
        average_confidence = confidence_scores.mean()

        return average_confidence