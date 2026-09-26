# Enterprise AI Assistant

A production-oriented Enterprise AI Assistant built with Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), vector search, tool calling, structured outputs, guardrails, authorization, and FastAPI.

The project demonstrates how modern Generative AI components can be combined into a secure AI application capable of answering company-policy questions and performing authorized employee operations.

## Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │ Input Guardrail │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ Intent Router   │
                  │ Structured      │
                  │ Output          │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
        Knowledge Query            Action Request
              │                         │
              ▼                         ▼
             RAG                       TOOL
              │                         │
              ▼                         ▼
        Qdrant Vector DB          Authorization
              │                         │
              └────────────┬────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Output Guardrail│
                  └────────┬────────┘
                           ▼
                         USER

