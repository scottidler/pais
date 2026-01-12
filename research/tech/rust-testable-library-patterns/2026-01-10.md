# Rust Testable Library Patterns

## Concise Guidelines for Agentic LLM Code Generation

### Error Handling Rules

1. **Never use `.unwrap()` or `.expect()` in lib/ code** - Always return `Result<T, E>`
2. **Use `thiserror` for custom error types** - Libraries need typed, matchable errors
3. **Map errors at boundaries** - Convert external errors to your domain errors with `#[from]`
4. **Propagate with `?`** - Let callers decide how to handle failures

### Error Type Pattern

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum LibError {
    #[error("invalid input: {0}")]
    InvalidInput(String),

    #[error("operation failed: {context}")]
    OperationFailed { context: String, code: u32 },

    #[error("io error")]
    Io(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, LibError>;
```

### Testability Architecture

1. **Define traits for external dependencies** - File I/O, network, time, randomness
2. **Accept `impl Trait` or `&dyn Trait` parameters** - Not concrete types
3. **Pure functions for core logic** - Input → Output, no side effects
4. **Thin integration layer** - Only wires dependencies together

### Dependency Injection Pattern

```rust
// Trait abstraction
pub trait DataStore {
    fn get(&self, id: &str) -> Result<Option<Data>>;
    fn put(&self, data: &Data) -> Result<()>;
}

// Pure business logic - highly testable
pub fn process_data(store: &impl DataStore, id: &str) -> Result<ProcessedData> {
    let data = store.get(id)?.ok_or(LibError::NotFound(id.into()))?;
    // Pure transformation logic
    Ok(transform(data))
}

// Test with mock
#[cfg(test)]
struct MockStore { data: HashMap<String, Data> }

#[cfg(test)]
impl DataStore for MockStore {
    fn get(&self, id: &str) -> Result<Option<Data>> {
        Ok(self.data.get(id).cloned())
    }
    fn put(&self, data: &Data) -> Result<()> { Ok(()) }
}
```

### Side Effect Isolation

```rust
// BAD - side effects embedded
fn process(path: &Path) {
    let content = std::fs::read_to_string(path).unwrap(); // side effect + panic
    println!("Result: {}", transform(&content)); // side effect
}

// GOOD - pure core, effects at edges
fn transform(input: &str) -> Result<Output> {
    // Pure logic only
}

fn process(reader: &impl Read, writer: &mut impl Write) -> Result<()> {
    let mut content = String::new();
    reader.read_to_string(&mut content)?;
    let output = transform(&content)?;
    writeln!(writer, "Result: {}", output)?;
    Ok(())
}
```

### Coverage Strategy

1. **Unit test pure functions exhaustively** - Easy 90%+ coverage
2. **Test error paths explicitly** - Each `Result::Err` variant
3. **Property-based testing** - Use `proptest` for edge cases
4. **Integration tests minimal** - Only test wiring, not logic
5. **Doc tests for public API** - Examples that compile and pass

### File Structure

```
src/
├── lib.rs           # Public API, re-exports
├── error.rs         # Error types with codes
├── traits.rs        # Abstractions for dependencies
├── core/            # Pure business logic (most code here)
│   ├── mod.rs
│   └── *.rs
└── adapters/        # Concrete implementations of traits
    ├── mod.rs
    └── *.rs

tests/
└── integration.rs   # Wiring tests only
```

### Quick Reference

| Instead of | Use |
|------------|-----|
| `.unwrap()` | `?` with `Result` |
| `.expect("msg")` | `.map_err(\|e\| LibError::Context { .. })?` |
| `panic!()` | Return `Err(LibError::...)` |
| `println!()` | `impl Write` parameter |
| `std::fs::*` direct | Trait abstraction |
| Concrete types | `impl Trait` parameters |
| `process::exit()` | Return error code in `Result` |

## Sources

- [Rust Error Handling: thiserror vs anyhow](https://momori.dev/posts/rust-error-handling-thiserror-anyhow/)
- [Make Rust Code Testable with Dependency Inversion](https://worldwithouteng.com/articles/make-your-rust-code-unit-testable-with-dependency-inversion/)
- [Rust Design-for-Testability Survey](https://alastairreid.github.io/rust-testability/)
- [GreptimeDB Error Handling Practices](https://greptime.com/blogs/2024-05-07-error-rust)
- [Rust Traits and Dependency Injection](https://jmmv.dev/2022/04/rust-traits-and-dependency-injection.html)
