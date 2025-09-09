function Button({ children, onClick, disabled, type = 'button' }) {
  return (
    <button type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

export default Button;