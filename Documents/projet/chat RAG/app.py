import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# ==========================================
# Configuration de la page Streamlit
# ==========================================
st.set_page_config(page_title="Docu-Chat 🤖", layout="wide")

# CSS personnalisé pour améliorer l'UI
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #2980b9;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Titre de l'application
# ==========================================
st.title("📄 Docu-Chat : Discutez avec vos PDF")
st.markdown("---")

# ==========================================
# Sidebar : Configuration et Upload
# ==========================================
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Champ pour la clé API OpenAI (type password pour la sécurité)
    api_key = st.text_input("Clé API OpenAI", type="password", help="Entrez votre clé sk-...")
    
    st.markdown("---")
    st.header("📂 Document")
    
    # Widget d'upload de fichier PDF
    uploaded_file = st.file_uploader("Uploadez votre PDF ici", type="pdf")

# ==========================================
# Vérification de la Clé API
# ==========================================
if not api_key:
    st.warning("⚠️ Veuillez entrer votre clé API OpenAI dans la barre latérale pour continuer.")
    st.stop()  # Arrête l'exécution du script ici si pas de clé

# Configuration de la clé pour LangChain
os.environ["OPENAI_API_KEY"] = api_key

# ==========================================
# Logique RAG (Retrieval Augmented Generation)
# ==========================================

@st.cache_resource(show_spinner=False)
def process_pdf(file):
    """
    Fonction pour traiter le PDF : sauvegarde temporaire, chargement, découpage et vectorisation.
    Utilise @st.cache_resource pour ne pas re-calculer à chaque interaction si le fichier ne change pas.
    """
    with st.spinner("⏳ Analyse du document en cours..."):
        try:
            # 1. Sauvegarde du fichier uploadé dans un fichier temporaire
            # Cela est nécessaire car PyPDFLoader attend un chemin de fichier
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file_path = tmp_file.name

            # 2. Chargement du PDF
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()

            # 3. Découpage du texte en morceaux (chunks)
            # chunk_size=1000 : taille des morceaux
            # overlap=200 : chevauchement pour garder le contexte entre les morceaux
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)

            # 4. Création de la base vectorielle (Embeddings)
            # Utilisation de OpenAIEmbeddings pour transformer le texte en vecteurs
            embeddings = OpenAIEmbeddings()
            
            # Création de ChromaDB en mémoire (pas de persist_directory)
            vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)

            # Nettoyage du fichier temporaire
            os.remove(tmp_file_path)

            return vectorstore

        except Exception as e:
            st.error(f"Une erreur est survenue lors du traitement du PDF : {e}")
            return None

# Initialisation de la session state pour l'historique (optionnel mais recommandé pour un chat)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Traitement du fichier si uploadé
if uploaded_file:
    vectorstore = process_pdf(uploaded_file)
    
    if vectorstore:
        st.success("✅ Document chargé et indexé avec succès !")

        # ==========================================
        # Interface de Chat
        # ==========================================
        
        # Champ de saisie pour la question de l'utilisateur
        query = st.chat_input("Posez votre question sur le document...")

        # Affichage de l'historique des messages (Bonus UX)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if query:
            # Affichage de la question de l'utilisateur
            with st.chat_message("user"):
                st.markdown(query)
            st.session_state.messages.append({"role": "user", "content": query})

            # Génération de la réponse
            with st.chat_message("assistant"):
                with st.spinner("🤖 Réflexion en cours..."):
                    # Création du modèle de chat
                    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
                    
                    # Chaîne de RetrievalQA
                    # chain_type="stuff" : insère tous les documents pertinents dans le prompt
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=vectorstore.as_retriever(),
                        return_source_documents=True # Important pour récupérer les sources
                    )

                    # Exécution de la chaîne
                    result = qa_chain.invoke({"query": query})
                    answer = result["result"]
                    source_documents = result["source_documents"]

                    # Affichage de la réponse
                    st.markdown(answer)
                    
                    # Affichage des sources dans un expander
                    with st.expander("📚 Sources utilisées"):
                        for i, doc in enumerate(source_documents):
                            st.markdown(f"**Source {i+1} :** (Page {doc.metadata.get('page', 'N/A') + 1})")
                            st.text(doc.page_content[:500] + "...") # Affiche les 500 premiers caractères du chunk
            
            # Ajout de la réponse à l'historique
            st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    st.info("👆 Veuillez uploader un fichier PDF dans la barre latérale pour commencer.")

# Footer
st.markdown("---")
st.caption("Développé pour Portfolio GitHub - RAG avec LangChain & Streamlit")
