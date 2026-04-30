
if user_input:
    st.session_state.chat_history.append(f"You: {user_input}")

    # If Confluence link is pasted
    if "atlassian.net/wiki" in user_input:
        page_id = extract_page_id(user_input)

        if page_id:
            bot_reply = process_confluence_page(page_id)
        else:
            bot_reply = "❌ Invalid Confluence URL"

    else:
        chunks = st.session_state.get("confluence_chunks", [])

        if not chunks:
            # fallback to your original chatbot behavior
            if any(keyword in user_input.lower() for keyword in [
                "who built", "who created", "developer", "author", "who made"
            ]):
                bot_reply = "This app was built by Nirmal Kallore 👨‍💻"
            else:
                prompt = "Always reply in English.\n" + "\n".join(st.session_state.chat_history)
                response = llm.invoke(prompt)
                bot_reply = response.content
        else:
            # Confluence-based QA
            relevant_chunks = get_relevant_chunks(chunks, user_input)

            context = "\n\n".join(relevant_chunks)

            prompt = f"""
            Answer ONLY using this context:

            {context}

            Question:
            {user_input}
            """

            response = llm.invoke(prompt)
            bot_reply = response.content

    st.session_state.chat_history.append(f"Angel: {bot_reply}")
