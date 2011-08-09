my.ellipse <- function(x, y, level = 0.75, segments = 51){
	dfn <- 2
    dfd <- length(x) - 1
    if (dfd < 3){
    	ellipse <- rbind(c(NA,NA))	
    } else {
        require(MASS)
        v <- cov.trob(cbind(x, y))
        shape <- v$cov
        center <- v$center
        radius <- sqrt(dfn * qf(level, dfn, dfd))
        angles <- (0:segments) * 2 * pi/segments
    	unit.circle <- cbind(cos(angles), sin(angles))
	    ellipse <- t(center + radius * t(unit.circle %*% chol(shape)))
    }
    
    ellipse <- as.data.frame(ellipse)
    colnames(ellipse) <- c("x","y")
    return(ellipse)
}

StatEllipse <- proto(Stat,
	{
		required_aes <- c("x", "y")
		default_geom <- function(.) GeomPath
		objname <- "ellipse"

		calculate_groups <- function(., data, scales, ...){
			.super$calculate_groups(., data, scales,...)
		}
		calculate <- function(., data, scales, level = 0.75, segments = 51,...){
			my.ellipse(data$x, data$y, level = level, segments = segments)	
		}
	}
)

stat_ellipse <- StatEllipse$build_accessor()
