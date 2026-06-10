"""
Tests for Mem0 LEGO Pieces — AI Earth Platform
================================================
Tests all extracted Mem0 components to verify they work correctly.
Source: https://github.com/mem0ai/mem0 (48K ⭐)
"""

import sys
import os
import pytest

# Ensure paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ai_earth', 'lego', 'stubs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ai_earth', 'lego'))


# ══════════════════════════════════════════════════════════════════════
# 1. EXCEPTIONS
# ══════════════════════════════════════════════════════════════════════

class TestExceptions:
    """Test Mem0 exception hierarchy."""

    def test_memory_error(self):
        from mem0.exceptions import MemoryError
        assert issubclass(MemoryError, Exception)

    def test_authentication_error(self):
        from mem0.exceptions import AuthenticationError, MemoryError
        assert issubclass(AuthenticationError, MemoryError)

    def test_rate_limit_error(self):
        from mem0.exceptions import RateLimitError, MemoryError
        assert issubclass(RateLimitError, MemoryError)

    def test_validation_error(self):
        from mem0.exceptions import ValidationError, MemoryError
        assert issubclass(ValidationError, MemoryError)

    def test_memory_not_found_error(self):
        from mem0.exceptions import MemoryNotFoundError, MemoryError
        assert issubclass(MemoryNotFoundError, MemoryError)

    def test_llm_error(self):
        from mem0.exceptions import LLMError, MemoryError
        assert issubclass(LLMError, MemoryError)

    def test_embedding_error(self):
        from mem0.exceptions import EmbeddingError, MemoryError
        assert issubclass(EmbeddingError, MemoryError)

    def test_vector_store_error(self):
        from mem0.exceptions import VectorStoreError, MemoryError
        assert issubclass(VectorStoreError, MemoryError)

    def test_database_error(self):
        from mem0.exceptions import DatabaseError, MemoryError
        assert issubclass(DatabaseError, MemoryError)

    def test_dependency_error(self):
        from mem0.exceptions import DependencyError, MemoryError
        assert issubclass(DependencyError, MemoryError)

    def test_network_error(self):
        from mem0.exceptions import NetworkError, MemoryError
        assert issubclass(NetworkError, MemoryError)


# ══════════════════════════════════════════════════════════════════════
# 2. CONFIGS
# ══════════════════════════════════════════════════════════════════════

class TestConfigs:
    """Test Mem0 configuration system."""

    def test_memory_type_enum(self):
        from mem0.configs.enums import MemoryType
        assert hasattr(MemoryType, 'PROCEDURAL')
        assert hasattr(MemoryType, 'EPISODIC')
        assert hasattr(MemoryType, 'SEMANTIC')

    def test_memory_config(self):
        from mem0.configs.base import MemoryConfig
        config = MemoryConfig()
        assert config is not None

    def test_memory_item(self):
        from mem0.configs.base import MemoryItem
        assert MemoryItem is not None

    def test_prompts(self):
        from mem0.configs.prompts import FACT_RETRIEVAL_PROMPT
        assert FACT_RETRIEVAL_PROMPT is not None
        assert isinstance(FACT_RETRIEVAL_PROMPT, str)


# ══════════════════════════════════════════════════════════════════════
# 3. MEMORY BASE
# ══════════════════════════════════════════════════════════════════════

class TestMemoryBase:
    """Test memory base classes."""

    def test_memory_base(self):
        from mem0.memory.base import MemoryBase
        assert MemoryBase is not None

    def test_sqlite_manager(self):
        from mem0.memory.storage import SQLiteManager
        assert SQLiteManager is not None

    def test_memory_utils(self):
        from mem0.memory.utils import parse_vision_messages
        assert callable(parse_vision_messages)


# ══════════════════════════════════════════════════════════════════════
# 4. EMBEDDINGS
# ══════════════════════════════════════════════════════════════════════

class TestEmbeddings:
    """Test embedding providers."""

    def test_embedding_base(self):
        from mem0.embeddings.base import EmbeddingBase
        assert EmbeddingBase is not None

    def test_embedding_configs(self):
        from mem0.embeddings.configs import EmbedderConfig
        assert EmbedderConfig is not None

    def test_openai_embedding_importable(self):
        from mem0.embeddings.openai import OpenAIEmbedding
        assert OpenAIEmbedding is not None

    def test_mock_embedding(self):
        from mem0.embeddings.mock import MockEmbeddings
        assert MockEmbeddings is not None


# ══════════════════════════════════════════════════════════════════════
# 5. LLMs
# ══════════════════════════════════════════════════════════════════════

class TestLLMs:
    """Test LLM providers."""

    def test_llm_base(self):
        from mem0.llms.base import LLMBase
        assert LLMBase is not None

    def test_llm_configs(self):
        from mem0.llms.configs import LlmConfig
        assert LlmConfig is not None

    def test_openai_llm_importable(self):
        from mem0.llms.openai import OpenAILLM
        assert OpenAILLM is not None


# ══════════════════════════════════════════════════════════════════════
# 6. VECTOR STORES
# ══════════════════════════════════════════════════════════════════════

class TestVectorStores:
    """Test vector store providers."""

    def test_vector_store_base(self):
        from mem0.vector_stores.base import VectorStoreBase
        assert VectorStoreBase is not None

    def test_vector_store_configs(self):
        from mem0.vector_stores.configs import VectorStoreConfig
        assert VectorStoreConfig is not None


# ══════════════════════════════════════════════════════════════════════
# 7. RERANKER
# ══════════════════════════════════════════════════════════════════════

class TestRerankers:
    """Test reranker components."""

    def test_base_reranker(self):
        from mem0.reranker.base import BaseReranker
        assert BaseReranker is not None

    def test_zero_entropy_reranker(self):
        from mem0.reranker.zero_entropy_reranker import ZeroEntropyReranker
        assert ZeroEntropyReranker is not None

    def test_llm_reranker(self):
        from mem0.reranker.llm_reranker import LLMReranker
        assert LLMReranker is not None


# ══════════════════════════════════════════════════════════════════════
# 8. UTILS (Factories, Scoring, Entity Extraction)
# ══════════════════════════════════════════════════════════════════════

class TestUtils:
    """Test utility modules."""

    def test_llm_factory(self):
        from mem0.utils.factory import LlmFactory
        assert LlmFactory is not None

    def test_embedder_factory(self):
        from mem0.utils.factory import EmbedderFactory
        assert EmbedderFactory is not None

    def test_vector_store_factory(self):
        from mem0.utils.factory import VectorStoreFactory
        assert VectorStoreFactory is not None

    def test_reranker_factory(self):
        from mem0.utils.factory import RerankerFactory
        assert RerankerFactory is not None

    def test_load_class(self):
        from mem0.utils.factory import load_class
        assert callable(load_class)

    def test_scoring(self):
        from mem0.utils.scoring import score_and_rank
        assert callable(score_and_rank)

    def test_bm25_params(self):
        from mem0.utils.scoring import get_bm25_params
        params = get_bm25_params("hello world")
        assert isinstance(params, tuple)

    def test_entity_extraction(self):
        from mem0.utils.entity_extraction import extract_entities
        assert callable(extract_entities)

    def test_lemmatization(self):
        from mem0.utils.lemmatization import lemmatize_for_bm25
        assert callable(lemmatize_for_bm25)


# ══════════════════════════════════════════════════════════════════════
# 9. CLIENT
# ══════════════════════════════════════════════════════════════════════

class TestClient:
    """Test Mem0 client."""

    def test_client_types(self):
        from mem0.client.types import AddMemoryOptions
        assert AddMemoryOptions is not None

    def test_client_utils(self):
        from mem0.client.utils import api_error_handler
        assert callable(api_error_handler)


# ══════════════════════════════════════════════════════════════════════
# 10. PROXY
# ══════════════════════════════════════════════════════════════════════

class TestProxy:
    """Test Mem0 proxy module."""

    def test_proxy_main_exists(self):
        import os
        proxy_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'ai_earth', 'lego', 'mem0', 'proxy', 'main.py'
        )
        assert os.path.exists(proxy_path)


# ══════════════════════════════════════════════════════════════════════
# 11. INTEGRATION — Mem0 + DSPy + EvoAgentX
# ══════════════════════════════════════════════════════════════════════

class TestMem0Integration:
    """Test that Mem0, DSPy, and EvoAgentX work together."""

    def test_all_three_packages(self):
        import dspy
        import evoagentx
        from mem0.exceptions import MemoryError
        assert dspy is not None
        assert evoagentx is not None
        assert MemoryError is not None

    def test_mem0_with_dspy_types(self):
        from mem0.configs.base import MemoryConfig
        from dspy.primitives.example import Example
        config = MemoryConfig()
        e = Example(memory="test")
        assert config is not None
        assert e.memory == "test"

    def test_mem0_with_evoagentx_memory(self):
        from mem0.configs.base import MemoryConfig
        from evoagentx.memory.memory import ShortTermMemory
        mc = MemoryConfig()
        stm = ShortTermMemory()
        assert mc is not None
        assert stm is not None
