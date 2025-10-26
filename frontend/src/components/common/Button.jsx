import PropTypes from 'prop-types';

function Button({ children, onClick, disabled, type = 'button' }) {
  return (
    <button type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

Button.propTypes = {
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func, 
  disabled: PropTypes.bool,
  type: PropTypes.oneOf(['button', 'submit', 'reset']), 
};


export default Button;