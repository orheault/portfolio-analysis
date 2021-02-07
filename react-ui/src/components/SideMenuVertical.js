export const SideMenuVertical = (props) => {

    return (
        <div className={`ui menu sidebar left vertical pointing inverted animating ${props.toggleMenu ? 'visible' : ''}`}>
            <div className="item link">Item 1</div>
            <div className="item link">Item 2</div>
        </div>
    )
} 